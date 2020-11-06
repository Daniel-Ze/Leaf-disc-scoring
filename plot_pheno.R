#!/usr/bin/Rscript
library(ggplot2)
library(readr)
library(R.utils)

results <- cmdArg("r")

results_file_path <- dirname( results )
results_file_name <- basename( results )

results_tbl <- read.table( results,
                           header = TRUE,
                           sep = "\t")

ggplot(results_tbl, aes(x=Exp_name,y=perc_spo))+
     geom_violin()+
     geom_boxplot(width = 0.2, alpha = 0.5)+
     geom_jitter(width = 0.2)+
     theme_bw()+
     theme(axis.title.x = element_blank())+
     ylab("% leaf with sporangia")+
     ggtitle("Phenotypic score distribution")

ggsave(paste0(results_file_path,"/results/pheno_score_plot.png"),
      width = 4,
      height = 4)
