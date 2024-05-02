#include <iostream>
#include <vector>
#include <algorithm>
#include <omp.h>

using namespace std;

bool isFibonacci(int n) {
    if (n < 0) return false;
    int a = 0, b = 1;
    while (b <= n) {
        if (b == n || a == n) return true;
        int temp = b;
        b = a + b;
        a = temp;
    }
    return false;
}

int main() {
    int N;
    cout << "Enter the maximum number (N) to check for Fibonacci numbers: ";
    cin >> N;

    vector<int> fibonacciNumbers;
    omp_set_num_threads(2); // Set the number of threads here

    double start_time = omp_get_wtime(); // Start timing

    #pragma omp parallel
    {
        vector<int> localFibonacci;
        #pragma omp for nowait
        for (int i = 0; i <= N; ++i) {
            if (isFibonacci(i)) {
                localFibonacci.push_back(i);
            }
        }
        
        #pragma omp critical
        {
            fibonacciNumbers.insert(fibonacciNumbers.end(), localFibonacci.begin(), localFibonacci.end());
        }
    }

    sort(fibonacciNumbers.begin(), fibonacciNumbers.end()); // Ensuring the numbers are sorted

    double end_time = omp_get_wtime(); // End timing

    cout << "Fibonacci numbers up to " << N << " are: ";
    for (int num : fibonacciNumbers) {
        cout << num << " ";
    }
    cout << endl;

    cout << "Elapsed time: " << end_time - start_time << " seconds." << endl;

    return 0;
}

/*g++ -fopenmp -o fibonacci lab2.2.cpp  
 ./fibonacci*/