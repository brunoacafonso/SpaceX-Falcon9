# SpaceX Falcon 9
 In this repository, I am using SpaceX Falcon 9 launch data to predict landing success of a launch.
 This project is based on the [Applied Data Science Capstone](https://www.coursera.org/learn/applied-data-science-capstone?specialization=ibm-data-science) course, which is the last course of Coursera's [Data Science Professional Certificate](https://www.coursera.org/professional-certificates/ibm-data-science).
 
 However, I have improved not only many of the analyses in order to improve that prediction, but I have also increased the detail in the explanations of what is being done in each line of code. This repository is composed of an introduction/methodology file, several exploratory data analyses files and a results/discussion file coming from the modeling approaches used.
 
 ## Contents
 ### The Problem and The Approach
 Introduction to the problem and general methodology used.
 
 ### Exploring and Preparing Data
 Exploratory data analysis and data preparation for model development.
 
 ### Model Development
 Data standardization, split into training and test data, model fit using logistic regression, decision tree, support vector machine and $k$-nearest neighbours. This file also includes details on the hyperparameter grids used in each model.
 
 ### Webscraping Falcon 9 and Heavy Falcon launches
 An alternative way to obtain data on SpaceX launches. Instead of using the API from the SpaceX website, in this file the data was scraped from a Wikipedia web page.
