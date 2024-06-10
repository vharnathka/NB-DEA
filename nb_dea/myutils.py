import sys
import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy.stats import chi2
from statsmodels.stats.multitest import multipletests
from scipy.optimize import minimize
from statsmodels.tools.sm_exceptions import PerfectSeparationError


def PREPROCESS(samplenumA, samplenumB):
    og_input = pd.read_csv("nb-deainput.csv", index_col=0)
    
    samplestotal = samplenumA+samplenumB
    counts = og_input.iloc[:, samplestotal: 2*samplestotal]
    avglength = og_input.iloc[:, 2*samplestotal: 3*samplestotal]
    
    return counts, avglength


def FILTER(counts, avglength, threshold):
    counts['Total'] = counts.sum(axis=1)

    rows_to_drop = counts[counts['Total'] < threshold].index.tolist()

    counts.drop(rows_to_drop, inplace=True)
    counts.drop('Total', axis=1, inplace=True)

    avglength.drop(rows_to_drop, inplace=True)
    
    return counts, avglength

def NORMALIZE(counts, samplestotal):
    ##using a geometric mean
    counts2 = counts.copy()
    arr_counts = counts2.to_numpy()
    arr_counts[arr_counts == 0] = 1

    pseudoref = np.prod(arr_counts, axis=1)**(1/samplestotal)
    counts2["Psuedo-Reference"] = pseudoref

    #ratios of each sample to reference
    for i in range(samplestotal):
        colname = counts.columns[i]
        counts2['ratio.' + str(i+1)] = counts2[colname]/counts2["Psuedo-Reference"]
        #median of each column is that sample's sizefactor
        median = counts2['ratio.' + str(i+1)].median()
    
        #divide by size factor
        counts[colname] = counts[colname]/median
    
    #taking care of zeros
    pseudocounts = 1e-6
    counts+=1e-6
    return counts

    
def estimate_dispersion(df):
    def neg_log_likelihood(params, counts):
        mean = np.mean(counts)
        dispersion = params[0]
        n = len(counts)
        log_likelihood = np.sum(counts * np.log(mean) - (counts + 1/dispersion) * np.log(1 + mean * dispersion))
        return -log_likelihood
    dispersions = []
    for gene in df.index:
        counts = df.loc[gene].values
        result = minimize(neg_log_likelihood, x0=[1.0], args=(counts,), bounds=[(1e-10, None)])
        dispersions.append(result.x[0])
    return np.array(dispersions)

def fit_negative_binomial(df, num_untreated_replicates, num_treated_replicates, stats):
    results = {}
    group = np.array([0] * num_untreated_replicates + [1] * num_treated_replicates)
    skipped_genes = []
    for gene in df.index:
        counts = df.loc[gene].values 
        try:
            model = sm.GLM(counts, sm.add_constant(group), family=sm.families.NegativeBinomial(alpha=stats['dispersion'][gene]))
            result = model.fit()
            results[gene] = result
        except PerfectSeparationError:
            skipped_genes.append(gene)
    with open('skipped_genes.txt', 'w') as f:
        f.write('These genes were skipped because their counts were too low:\n')
        for item in skipped_genes:
            f.write(f"{item}\n")
    return results

def test_differential_expression(fit_results, num_untreated_replicates, num_treated_replicates, stats, df):
    p_values = {}
    log2_fold_changes = {}
    group = np.array([0] * num_untreated_replicates + [1] * num_treated_replicates)
    null_group = np.zeros_like(group)
    for gene, result in fit_results.items():
        counts = df.loc[gene].values
        llf_alt = result.llf
        null_model = sm.GLM(counts, sm.add_constant(null_group), family=sm.families.NegativeBinomial(alpha=stats['dispersion'][gene]))
        null_result = null_model.fit()
        llf_null = null_result.llf
        lr_stat = 2 * (llf_alt - llf_null)
        p_value = chi2.sf(lr_stat, df=1)
        p_values[gene] = p_value
        
        mean_treated = np.mean(counts[group == 1])
        mean_untreated = np.mean(counts[group == 0])
        log2_fold_change = np.log2(mean_treated / mean_untreated)
        log2_fold_changes[gene] = log2_fold_change

    return p_values, log2_fold_changes

def NBA(counts, samplenumA, samplenumB):
    #dispersion
    stats = counts.copy()
    stats = stats.iloc[:, 0:0]
    stats['dispersion'] = estimate_dispersion(counts)
    #fitting to neg binomial model
    fit_results = fit_negative_binomial(counts, samplenumA, samplenumB, stats)
    
    #getting p-vals, log2 fold changes
    p_values, log2_fold_changes = test_differential_expression(fit_results, samplenumA, samplenumB, stats, counts)
    rejected, adj_p_values, _, _ = multipletests(list(p_values.values()), method='fdr_bh')
    adj_p_values_dict = dict(zip(p_values.keys(), adj_p_values))
    
    results_df = pd.DataFrame({
    'log2FoldChange': log2_fold_changes,
    'pvalue': p_values,
    'padj': adj_p_values_dict
})
    
    return results_df
    #results_df.to_csv('differential_expression_results.csv', index=True)