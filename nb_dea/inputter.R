perform_tximport <- function(files, conditions) {
    ##### Load the libraries we need #####
    suppressMessages({
        suppressWarnings({
            
        
            library("tximport")
            library("readr")
         

            files_r <- as.character(files)
            ##### Create a dataframe for samples #####
            samples <- data.frame("run" = basename(files_r), "condition"=conditions)
            names(files) = samples$run
            
            # Import RSEM results with tximport
            txi <- tximport(files_r, type = "rsem")
          
            # Add a pseudocount of 1 to fix an error with 0-length transcripts
            txi$length[txi$length == 0] <- 1
    
            write.csv(txi, file="nb-deainput.csv")
        })
    })
}