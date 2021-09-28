# Knowledge
📚 Represent personal Knowledge as a graph, with nodes for tags and edges for connections between them. The connections are computed based on the number of articles in commun for one tag. This should serve as a way to discover visually new content, and browse through existing content.

![graph_top10](img/graph_top10.gif)

## Processing Workflow
![processing_flow](img/processing_flow.png)

## Tag generation

### Manually

Services like [Diigo](https://www.diigo.com/) can be used to save and tag online resources manually.

### Automatically

Tags can be automatically generated via supervised classification methods:

1. *Training*
![supervised_classification_step1](img/supervised_classification_step1.png)

2. *Inference*
![supervised_classification](img/supervised_classification.png)



## Graph drawing

Based on the list of articles and tags, two types of graphs can be drawn; a graph of articles, or a graph of tags - representing the corpus (workflow detailed here):

1. First representing an article as a vector

<img src="img/file_1.png" height=20px> [Knowledge Graph - Wikipedia, the free encyclopedia](http://en.wikipedia.org/wiki/Knowledge_Graph)

Tags: __google__ __wikipedia__ __science__ 

<img src="img/file_1_vector.png" width=300px>

2. Second building the [adjacency matrix](https://en.wikipedia.org/wiki/Adjacency_matrix):
Depending on how the matrix is computed, the nodes are either the articles or the tags.
In this example, the nodes are the tags:

    **Z55 = T59*T95**

<img src="img/adjacency_matrix_building.png" width=600px>

3. Third drawing the graph from the adjacency matrix

<img src="img/adjacency_matrix_to_graph.png">

## Previous implementations

- Article graph

![article_graph](img/article_graph.png)

- Tag graph

![tag_graph](img/tag_graph.png)


## References:

- Fundamentals of Predictive Text mining