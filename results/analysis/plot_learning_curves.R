library(tidyverse)
library(ggplot2)

theme_set(theme_bw())

this.dir <- dirname(rstudioapi::getSourceEditorContext()$path)
setwd(this.dir)

for (p in dir(path = "../", pattern = "*.csv")) {
  d = read.csv(paste("../", p, sep=""))
  d = d %>% pivot_longer(-iteration, names_to="metric")
  
  plt = d %>% ggplot(aes(x=iteration, y=value, col=metric)) + geom_line() + theme(legend.position = "bottom") + ggtitle(gsub(".csv", "", p))
  plot(plt)
  ggsave(paste(gsub(".csv", "", p), ".png", sep=""), plt)
  
}
