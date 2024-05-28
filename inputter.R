perform_tximport <- function(files, conditions) {
    ##### Load the libraries we need #####
    library("tximport")

    ##### Create a dataframe for samples #####
    samples <- data.frame("run" = basename(files), "condition" = conditions)
    
    # Import RSEM results with tximport
    txi <- tximport(files, type = "rsem")
    
    # Add a pseudocount of 1 to fix an error with 0-length transcripts
    txi$length[txi$length == 0] <- 1

    return(txi)
}