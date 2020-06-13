## Description
PageRank is an algorithm that will rank webpages by their importance represented by a probability (0-1.0)
- webpages' importance will be weightedly judged based on the amount and importance of webpages linking to themselves
- the program calculates for the pagerank using two methods
    - random sampling using Markov Chain
        - damping_factor is a changeable probability of a surfer going to the webpages only within the links
        - n represents the sample that will be taken, more sample would result in a more precise estimate
    - iterative algorithm
            - threshold delta can be changed in the while loop, the lower the value, the more precise the result
    
## Usage
```
$ python pagerank.py [directory]
```
- directory should contain webpages in terms of html files

```
$ python pagerank.py example
PageRank Results from Sampling (n = 10000)
  1.html: 0.2143
  2.html: 0.4292
  3.html: 0.2225
  4.html: 0.1341
PageRank Results from Iteration
  1.html: 0.2269
  2.html: 0.4407
  3.html: 0.2248
  4.html: 0.1330
```
