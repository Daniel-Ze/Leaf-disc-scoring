#!/usr/bin/Rscript
library(ggplot2)
library(readr)
library(R.utils)

coords <- cmdArg("c")

coord_file_path <- dirname( coords )
coord_file_name <- basename( coords )

coord_tbl <- read.table( coords,
                         header = FALSE,
                         sep = "\t" )


ggplot(coord_tbl,aes(coord_tbl$V1,coord_tbl$V2))+
  geom_point(shape = 0, colour = "black", fill = "white", size = 10, stroke = 2)+
  scale_x_continuous(breaks = c(0:23))+
  scale_y_continuous(breaks = c(0:22))+
  theme_bw()+
  ylab("y-axis")+
  xlab("x-axis")

ggsave(paste0(coord_file_path,"/results/",coord_file_name,"_plot.png"), width = 9, height = 8)
