Hi, this is README.

Environment: Mac OS 10.13.6  python2.7.10 

This is an implement for four different algorithms of uncertain inference in Bayesian networks. There are 4 files. enumeration_inference.py, likelihood_weighting.py, rejection_sampling.py and gibbs_sampling.py are implements for four different inference methods in Bayesian network. The folder examples contains three xml files which are examples of Bayesian network. The file xmlparser.py is a XML parser to read those files.

To run the program, enter the command line “enumeration_inference.py aima-alarm.xml B J true M true”. Which means you want to query for the aima-alarm file, the query variable is B and the observed variable is J is true M is true. For likelihood_weighting.py, rejection_sampling.py and gibbs_sampling.py use "gibbs_sampling.py 10000 aima-alarm.xml B J true M true" where 10000 is the number of samples you want to use.

              Copyright: 2018, Haoning Hu