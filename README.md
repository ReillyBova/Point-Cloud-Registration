# Point Cloud Registration
This repository contains a Python 3 script that implements the ICP (Iterative Closest Points) algorithm for the 3D registration of point clouds.

## Getting Started

Follow these instructions in order to run this script on your local machine (NB: this has only been tested on Mac OSX, but it should work for other systems).

### Prerequisites & Installation

This project only requires Python 3 and the [NumPy](http://www.numpy.org/) python library. It is suggested that users use pip3 to install NumPy.

### Running the Script

This script requires two pairs of files (a total of four files altogether) to run: `file1.pts`, `file1.xf`, `file2.pts`, and `file2.xf`. When run, the script will attempt to adjust the rigid body transform in file1.xf in order to align the points in file1.pts to the target points, which are the points from file2.pts transformed by the matrix in file2.xf. Finally, the script will output the results in `./output/`.

The program is executed as follows:

```
$ python3 icp.py file1.pts file2.pts
```

Note that the `.xf` files are implicit. The program will first look for `file.xf` in `./output/`, and then in the provided file path for the file. This is done to avoid overwriting aligned transformations with the original (inaccurrate) transformation.

## Program Explanation

### Implementation Details

This program utilizes a custom Python implementation of a KdTree, adapted and expanded from COS 226 assignment code and lectures. Unlike the introductory class assignment, it is a true KdTree in that it is able to handle points of any positive dimension `k`.

Additionally, this script heavily relies on the matrix manipulation and linear algebra methods provided by the NumPy library.

### Iterative Point Cloud Algorithm

During each ICP iteration, 1000 points are sampled at random from the source dataset (`file1`), and then each sampled point's nearest neighbor from the target dataset (`file2`) is computed. Then, outlier rejection is applied, and the remaining points are fed into the over-constrained linear system. Once this is solved, a new transformation matrix to apply on the source dataset is computed, and a new iteration cycle begins if significant improvement has been made. Otherwise, the ICP algorithm terminates with a rigid-body transformation matrix that align's the points in the source dataset with those in the target dataset.

Further details on this algorithm may be found [here](http://www.cs.princeton.edu/courses/archive/fall18/cos526/notes/cos526_f18_lecture10_acquisition_registration.pdf).

### Miscellaneous Notes

This program contains fairly robust error handling, however, it has not been rigorously tested for bugs.

## Results

|  Before | After | 
|:--------------:|:----------------:|
| ![Direct Cloning](/results/battleOfPrinceton_direct.png?raw=true) | ![Poisson Cloning](/results/battleOfPrinceton_poisson.png?raw=true) |
| ![Direct Cloning](/results/fig3a_direct.png?raw=true) | ![Poisson Cloning](/results/fig3a_poisson.png?raw=true) |
| ![Direct Cloning](/results/fig3b_direct.png?raw=true) | ![Poisson Cloning](/results/fig3b_poisson.png?raw=true) |
| ![Direct Cloning](/results/fig4_direct.png?raw=true) | ![Poisson Cloning](/results/fig4_poisson.png?raw=true) |

## Authors

* **Reilly Bova** - [ReillyBova](https://github.com/ReillyBova)

See also the list of [contributors](https://github.com/ReillyBova/Point-Cloud-Registration/contributors) who participated in this project.

## References
[1] Rusinkiewicz, M. Levoy, "Efficient variants of the ICP algorithm", Proc. 3rd Int. Conf. 3D Digital Imaging and Modeling, pp. 145-152, 2001.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

Thank you to Professor Szymon Rusinkiewicz for putting this assignment together for the Fall 2018 semester of COS 526: Advanced Computer Graphics
