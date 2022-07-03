#!/usr/bin/env Rscript
library(ggplot2)
library(readr)
library(R.utils)
library(ggpubr)
library(mclust)
library(cowplot)

# version 0.2
# license http://creativecommons.org/licenses/by-nc-sa/4.0/

# Clustering of individuals into groups:
#   - Using the number of images with and without spores
#   - Following the instructions given von the mclust website
# https://cran.r-project.org/web/packages/mclust/vignettes/mclust.html
# Histogram with density plot after clustering:
#   - Plotting the percent sporangiophore coverage on leaf discs
#   - Coloring the bar plots accordin to the assigned classes
# https://www.datanovia.com/en/blog/ggplot-histogram-with-density-curve-in-r-using-secondary-y-axis/

# Reading the command line input
results <- cmdArg("r")

results_file_path <- dirname( results )
results_file_name <- basename( results )

# Reading the file as a table
results_tbl <- read.table(results,
			  header = TRUE,
			  sep = "\t",
			  comment.char = "#")

# Getting the test name for plot titles
test_name<-noquote(results_tbl$Exp_name[1])

# Mclust part:
#   - Determine the model for clustering (BIC info: https://en.wikipedia.org/wiki/Bayesian_information_criterion)
#   - The number of sub images with and without infection are used for the model
#clPairs(results_tbl[,c(8,9)])            # for manual run of the script
BIC <- mclustBIC(results_tbl[,c(8,9)])
#plot(BIC)                                # for manual run of the script
#summary(BIC)                             # for manual run of the script
#   - Using the best BIC inferred model for clustering of the samples
mod1 <- Mclust(results_tbl[,c(8,9)], x = BIC)
#summary(mod1, parameters = TRUE)         # for manual run of the script
#plot(mod1, what = "classification")      # for manual run of the script
#   - Store the corresponding cluster information as class in the results table
results_tbl$class <- as.factor(mod1$classification)

# Create boxplot of the data as quick overview
pbox<-ggplot(results_tbl, aes(x=Exp_name,y=perc_spo))+
	geom_violin(alpha = 0.6)+
	geom_boxplot(width = 0.1, alpha = 0.5)+
	geom_jitter(width = 0.1, height = 0.01, color=results_tbl$class)+
	scale_y_continuous(limit = c(0, max(results_tbl$perc_spo)+10),
			   breaks = seq(0,max(results_tbl$perc_spo)+10,by = 20))+
	theme_bw()+
        theme(axis.title.x = element_blank(),
	      axis.text.x = element_text(size = 12))+
     	ylab("% coverage area")+
        ggtitle(paste(test_name,"- Phenotypic score distribution"))
  
# Create the histogram with overlaid density rug plot
#   - bars are filled according to the assigned classes from clustering
phist<-gghistogram(results_tbl, 
		   x = "perc_spo", 
                   add = "median", 
                   rug = TRUE,
                   fill = "class")+
	ylab("# Individuals")+
	xlab("% leaf disc with sporangiophores")+
	ggtitle(paste(test_name,"- Phenotypic score distribution"))
 
pdense<-ggdensity(results_tbl, 
                  x = "perc_spo",
                  color = "class",
                  alpha = 0)+
	scale_y_continuous(expand = expansion(mult = c(0.05, 0.05)), position = "right")  +
	theme_half_open(11, rel_small = 1) +
        rremove("x.axis")+
        rremove("xlab") +
	rremove("x.text") +
        rremove("x.ticks") +
	rremove("legend")
	     
aligned_plots<-align_plots(phist, pdense, align="hv", axis="tblr")
aligned_plots_final<-ggdraw(aligned_plots[[1]]) + draw_plot(aligned_plots[[2]])
	     
ggsave(plot = pbox, paste0(results_file_path,"/results/pheno_score_plot_test1.png"),
       width = 3,
       height = 5)

ggsave(plot = aligned_plots_final, paste0(results_file_path,"/results/pheno_score_plot_test2.png"),
       width = 10,
       height = 5)
