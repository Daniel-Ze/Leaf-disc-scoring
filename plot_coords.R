#!/usr/bin/env Rscript
library(ggplot2)
library(R.utils)
library(stringr)
library(jpeg)
library(grid)
# version 0.1
# license http://creativecommons.org/licenses/by-nc-sa/4.0/
#Grab the commandline input
coords <- cmdArg("c")

coord_file_path <- dirname( coords )
coord_file_name <- basename( coords )

#Refer to the image file from the coordinates
img_file_name <- unlist(strsplit(coord_file_name, "\\."))
img_file_name <- img_file_name[1]
img_file_path <- paste0(coord_file_path,"/",img_file_name,".jpg")

#Load the image file for the plot background
img <- jpeg::readJPEG(img_file_path)

#Load the coordinates as table
coord_tbl <- read.table( coords,
                         header = FALSE,
                         sep = "\t" )

#Plot the coordinates as squares
p1<-ggplot(coord_tbl,
           aes(coord_tbl$V1,
               coord_tbl$V2))+
           annotation_custom(rasterGrob(img,
                                        width = unit(0.95,"npc"),
                                        height = unit(0.95,"npc")),
                             -Inf, Inf, -Inf, Inf)+
           geom_point(shape = 0,
                      colour = "black",
                      fill = "white",
                      size = 8,
                      stroke = 2)+
           scale_x_continuous(limits=c(1,23),
                              breaks = c(seq(1, 23, 1)))+
           scale_y_continuous(limits=c(1,22),
                              breaks = c(seq(1, 22, 1)))+
           theme_bw()+
           ylab("y-axis")+
           xlab("x-axis")

#Save the plot to file
ggsave(file=paste0(coord_file_path,"/results/",coord_file_name,"_plot.png"),
      p1,
      width = 8,
      height = 7)
