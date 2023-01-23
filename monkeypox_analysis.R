library(jsonlite)
library(httr)
library(dplyr)
library(ggplot2)

base_url <- "http://127.0.0.1:8000/"

response <- GET(paste0(base_url, "latestdata/"))

result <- fromJSON(content(response, "text"))

df <- result$records

df <- df %>%
  mutate(Date = result$date)

ggplot(df) +
  geom_col(aes(x = `UK Nation`, y = Confirmed, fill = `UK Nation`)) +
  labs(title = paste("Date:", df$Date)) 

response2 <- GET(
  paste0(
  base_url, "search_range/?start_date=2022-10-25&end_date=2022-11-29"
  )
  )

result2 <- fromJSON(content(response2, "text"))

dfs = list()

for (i in 1:length(result2)){
  
  dfs[[i]] <- result2[[i]]$records %>%
    mutate(Date = result2[[i]]$date)
  
}

df2 <- bind_rows(dfs)

df3 <- df2 %>% group_by(`UK Nation`) %>% mutate(NewConfirmed=Confirmed-lag(Confirmed))

df3$Date <- as.Date(df3$Date)

ggplot(df3 %>% filter(`UK Nation` != "Total")) +
  geom_point(aes(x=Date, y=NewConfirmed, colour=`UK Nation`)) +
  facet_wrap(facets = vars(`UK Nation`))
  
