# Modeling Chaos in OpenGL

## Motivation
#### Logistic Map

![](screenshots/equation.svg)

This is the equation of the logistic map. x<sub>n+1</sub> where n is a step in a time unit. The value of x<sub>n+1</sub> can be found by multiplying the growth rate r with the current population and 1 minus the current population.

This equation can represent a nice simplified behavior in the change of population. Let's take the population of wolves for example. The current population of wolves will grow by a certain growth rate within a given amount of time. The more wolves there are the faster the population multiplies. The population will grow until there are too many wolves and not enough space, food, etc to support them all. At this point the population will decrease, this behavior is captured in the multiplication of 1 - x<sub>n</sub>.

#### Bifurcation Diagram
![](graphs/bifurcation_diagram.png)

At growth rate 2.8 the population settles to a single value. At 3.2 the population alternate between two different values. At 3.5 there is another split and the function alternates between 4 values. This division happens until chaos occurs. The grey spaces are where no pattern is found. The system eventually stabilizes. This can be seen in the white spaces in between blocks of chaos. The system alternates between fixed number of values until chaos hits again.

## Modelling this Diagram in 3D

I think it would be cool to model this diagram in three dimensions; x value being time, y being the population and z being the growth rate.

![](screenshots/1.png)
![](screenshots/2.png)
![](screenshots/3.png)

The beginning of the model shows nice waves, representing the system settling to a fix number of values. These waves are followed by chaotic spikes. In the last picture, we see the system once again settling only to be followed by chaos once again.

## Running the Code

```
>> g++ -std=c++11 common/shader.cpp common/controls.cpp chaos.cpp -framework OpenGL -framework Cocoa -framework IOKit -framework CoreVideo -lglfw3 -lglew

>> ./a.out
```

## Thank You and Further Reading

The majority of the code found in the common folder was learned from a great OpenGL tutorial. To learn more about OpenGL follow the link to this tutorial.

http://www.opengl-tutorial.org/