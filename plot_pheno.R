#!/usr/bin/env Rscript
library(ggplot2)
library(readr)
library(R.utils)

# version 0.1
# license http://creativecommons.org/licenses/by-nc-sa/4.0/

results <- cmdArg("r")

results_file_path <- dirname( results )
results_file_name <- basename( results )

results_tbl <- read.table( results,
                           header = TRUE,
                           sep = "\t",
                           comment.char = "#"
                         )

ggplot(results_tbl, aes(x=Exp_name,y=perc_spo))+
     geom_violin(alpha = 0.6)+
     geom_boxplot(width = 0.2, alpha = 0.5)+
     geom_jitter(width = 0.1, height = 0.01)+
     theme_bw()+
     theme(axis.title.x = element_blank())+
     ylab("% leaf with sporangia")+
     ggtitle("Phenotypic score distribution")

ggsave(paste0(results_file_path,"/results/pheno_score_plot.png"),
      width = 3,
      height = 5)
