#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>

/* Load the rigid body transformation from a provided .xf file as a 4x4 matrix
 * of homogenous coordinates
 */
std::vector<std::vector<double> > load_xf(std::string file_name)
{
  // Target data structure: a list of double arrays
  std::vector<std::vector<double> > transformation;

  // Load the file
  std::ifstream file(file_name);

  // Process file line by line
  std::string line;
  while (std::getline(file, line)) {

    // Read the values one at a time
    std::vector<double> lineData;
    std::stringstream lineStream(line);
    double val;
    while (lineStream >> val) {
      lineData.push_back(val);
    }

    // Enforce 6 args
    if (lineData.size() != 4) {
      fprintf(stderr, "Error: Read an xf line that did not have 4 parameters.\n");
      continue;
    }
    transformation.push_back(lineData);
  }

  return transformation;
}

// Load the points from a provided .pts file; returns a list of double arrays
std::vector<std::vector<double> > load_points(std::string file_name)
{
  // Target data structure: a list of double arrays
  std::vector<std::vector<double> > points;

  // Load the file
  std::ifstream file(file_name);

  // Process file line by line
  std::string line;
  while (std::getline(file, line)) {

    // Read the values one at a time
    std::vector<double> lineData;
    std::stringstream lineStream(line);
    double val;
    while (lineStream >> val) {
      lineData.push_back(val);
    }

    // Enforce 6 args
    if (lineData.size() != 6) {
      fprintf(stderr, "Error: Read a pts line that did not have 6 parameters.\n");
      continue;
    }
    points.push_back(lineData);
  }

  return points;
}

int main(int argc, char *argv[])
{
  std::vector<std::vector<double> > points = load_points("./bunny/bun000.pts");
  for (int i = 0; i < points.size(); i++) {
    for (int j = 0; j < points[i].size(); j++) {
      std::cout << points[i][j] << ' ';
    }
    std::cout << std::endl;
  }
  std::vector<std::vector<double> > xf = load_xf("./bunny/bun045.xf");
  for (int i = 0; i < xf.size(); i++) {
    for (int j = 0; j < xf[i].size(); j++) {
      std::cout << xf[i][j] << ' ';
    }
    std::cout << std::endl;
  }
}
