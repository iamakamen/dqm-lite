#include <cmath>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

#include "nlohmann/json.hpp"

using json = nlohmann::json;

struct Metrics {
    double mean;
    double stddev;
    int outlier_count;
    std::string status;
};

std::vector<double> read_values(const std::string &path) {
    std::vector<double> values;
    std::ifstream in(path);
    if (!in.is_open()) {
        throw std::runtime_error("Failed to open file: " + path);
    }

    double x;
    char comma;
    while (in >> x) {
        values.push_back(x);
        if (in.peek() == ',') {
            in >> comma;
        }
    }
    return values;
}

Metrics compute_metrics(const std::vector<double> &values) {
    if (values.empty()) {
        throw std::runtime_error("No data points in file.");
    }

    double sum = 0.0;
    for (double v : values) sum += v;
    double mean = sum / values.size();

    double sq_sum = 0.0;
    for (double v : values) {
        double diff = v - mean;
        sq_sum += diff * diff;
    }
    double variance = sq_sum / values.size();
    double stddev = std::sqrt(variance);

    int outlier_count = 0;
    const double k = 3.0; // 3-sigma rule
    for (double v : values) {
        if (std::fabs(v - mean) > k * stddev) {
            outlier_count++;
        }
    }

    // Simple quality rule: mean near 0 and few outliers
    std::string status = "GOOD";
    if (std::fabs(mean) > 2.0 || outlier_count > static_cast<int>(0.05 * values.size())) {
        status = "BAD";
    }

    return Metrics{mean, stddev, outlier_count, status};
}

int main(int argc, char **argv) {
    if (argc != 2) {
        std::cerr << "Usage: metrics_engine <path_to_csv>\n";
        return 1;
    }

    std::string path = argv[1];

    try {
        auto values = read_values(path);
        auto metrics = compute_metrics(values);

        json j;
        j["mean"] = metrics.mean;
        j["stddev"] = metrics.stddev;
        j["outlier_count"] = metrics.outlier_count;
        j["status"] = metrics.status;

        std::cout << j.dump() << std::endl;
    } catch (const std::exception &ex) {
        std::cerr << "Error: " << ex.what() << "\n";
        return 1;
    }

    return 0;
}
