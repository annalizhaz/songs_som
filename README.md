## Analysis of Million Songs Dataset: SOM Implementation

In this repository is an implementation of a Self-Organizing Map (SOM) used to aggregate the million song data, enabling comparision of song trends across time and genre.

### Algorithm Overview

A SOM is a data  visualization technique comprised of a self-organizing neural network. In brief, the map collapses vector  data into a two-dimensional space; each component node is then tuned according to input features, creating a topologically ordered map.

The basic implementation strategy was as follows: first, we cleaned and standardized the numeric song data. Our program then constructs a grid of nodes according to user-passed size variables. Each node represents a vector of length *n* - where *n* is the number of features in the sample data - and is initalized to a set of random values. 

For each complete pass of the song data (specified, again, by the user), we first compute a best matching unit (BMU) *c* for each song vector, defined as the grid node the shortest Euclidean distance from the passed input vector. Then, the grid weight vectors for each node *k* are updated for each input vector *t* according to the equation<sup>1</sup>:
<p align="center"><img src=https://latex.codecogs.com/gif.latex?w_k(t)=\frac{\sum_{t^{'}=0}^th_{ck}(t')\cdot&space;x(t')}{\sum_{t^{'}=0}^th_{ck}(t')}></p>
where the extent of a vector's weight response is controlled by the Gaussian neighborhood function:
<p align="center"><img src=https://latex.codecogs.com/gif.latex?h_{ck}(t)=\exp\bigg(\frac{\Vert&space;r_c-r_k\Vert^2}{\sigma(t)^2}\bigg)></p>

The Cartesian coordinates of *c* and *k* are given by <img src=https://latex.codecogs.com/gif.latex?r_c> and <img src=https://latex.codecogs.com/gif.latex?r_k>, respectively, and <img src=https://latex.codecogs.com/gif.latex?\sigma> is defined by the exponential decay function, assigned constants by the user:
<p align="center"><img src=https://latex.codecogs.com/gif.latex?\sigma(t)=\sigma_1\cdot&space;\bigg(\frac{\sigma_{t_f}}{\sigma_1}\bigg)^{\frac{t}{t_f}}></p>

<sup>1</sup>Christian Weichel, “Adapting Self-Organizing Maps to the MapReduce Programming Paradigm” (Paper presented  at the proceedings of Software-Technologien und Prozesse in Furtwangen, Germany. May 6, 2010).

*This repository represents part of a final project for Spring 2016 Computer Science with Applications III.*
