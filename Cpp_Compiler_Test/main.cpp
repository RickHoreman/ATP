#include "hwlib.hpp"
#include <charconv>
#include <array>

extern "C" void print(int n){
    hwlib::cout << n;
}

extern "C" int sadge_sensei_k();
extern "C" int sommig_sama(int n);
extern "C" int odd_tan(int n);
extern "C" int even_chan(int n);
extern "C" int recursiveExpression_oujosama_k();
extern "C" int compare_san(int n1, int n2, int mode);
extern "C" int forLoop_san(int startingValue, int increment, int controlValue, int mode);
extern "C" void printXtimes_chan(int n, int x);

// The following tests are made for examples/unit_tests.painandsuffering.
// Make sure the variable SADGE in Makefile has that file's relatvive path as value, otherwise these tests wont work for the most part.

int main(){
    hwlib::wait_ms(1000);

    hwlib::cout << "Print demo: \n";
    printXtimes_chan(10, 3); // This requires the extern C print function at line 5 to be defined.

    unsigned int passedTests = 0;
    unsigned int failedTests = 0;

    hwlib::cout << "\nCommencing tests.\n";

    // First off, the tests for the "test subroutines" we had to implement.
    if(odd_tan(1) != 1){
        hwlib::cout << "odd_tan(1) failed, expected '1', got '" << odd_tan(1) << "'.\n";
        failedTests++;
    }else{
        passedTests++;
    }
    if(odd_tan(0) != 0){
        hwlib::cout << "odd_tan(0) failed, expected '0', got '" << odd_tan(0) << "'.\n";
        failedTests++;
    }else{
        passedTests++;
    }
    if(odd_tan(-1) != -1){
        hwlib::cout << "odd_tan(-1) failed, expected '-1', got '" << odd_tan(-1) << "'.\n";
        failedTests++;
    }else{
        passedTests++;
    }
    if(odd_tan(-9000) != -1){
        hwlib::cout << "odd_tan(-9000) failed, expected '-1', got '" << odd_tan(-9000) << "'.\n";
        failedTests++;
    }else{
        passedTests++;
    }

    if(even_chan(1) != 0){
        hwlib::cout << "even_chan(1) failed, expected '0', got '" << even_chan(1) << "'.\n";
        failedTests++;
    }else{
        passedTests++;
    }
    if(even_chan(0) != 1){
        hwlib::cout << "even_chan(0) failed, expected '1', got '" << even_chan(0) << "'.\n";
        failedTests++;
    }else{
        passedTests++;
    }
    if(even_chan(-1) != -1){
        hwlib::cout << "even_chan(-1) failed, expected '-1', got '" << even_chan(-1) << "'.\n";
        failedTests++;
    }else{
        passedTests++;
    }
    if(even_chan(-9000) != -1){
        hwlib::cout << "even_chan(-9000) failed, expected '-1', got '" << even_chan(-9000) << "'.\n";
        failedTests++;
    }else{
        passedTests++;
    }

    std::array<int, 11>expected = {0, 1, 3, 6, 10, 15, 21, 28, 36, 45, 55};
    for(int i=0; i<11; i++){
        if(sommig_sama(i) != expected[i]){
            hwlib::cout << "sommig_sama(i) failed, expected '" << expected[i] << "', got '" << sommig_sama(i) << "'.\n";
            failedTests++;
        }else{
            passedTests++;
        }
    }
    if(sommig_sama(-1) != -1){
        hwlib::cout << "sommig_sama(-1) failed, expected '-1', got '" << sommig_sama(-1) << "'.\n";
        failedTests++;
    }else{
        passedTests++;
    }
    if(sommig_sama(-999) != -999){
        hwlib::cout << "sommig_sama(-999) failed, expected '-999', got '" << sommig_sama(-999) << "'.\n";
        failedTests++;
    }else{
        passedTests++;
    }

    // The following are extra functions I added to test specific functionality.

    // This one combines all "test subroutines":
    if(sadge_sensei_k() != 45){
        hwlib::cout << "sadge_sensei_k() failed, expected '45', got '" << sadge_sensei_k() << "'.\n";
        failedTests++;
    }else{
        passedTests++;
    }

    // This one contains a "recursive expression" I.E. expressions in expressions. The total expression even contains a function call.
    if(recursiveExpression_oujosama_k() != 4){
        hwlib::cout << "recursiveExpression_oujosama_k() failed, expected '4', got '" << recursiveExpression_oujosama_k() << "'.\n";
        failedTests++;
    }else{
        passedTests++;
    }

    // The following test logic operators (>, >=, <, <=) with modes (0, 1, 2, 3) respectively. (also testing if statements while we're at it)
    // First we test some base cases
    if(compare_san(1, 0, 0) != 1){
        hwlib::cout << "compare_san(1, 0, 0) failed, expected '1', got '" << compare_san(1, 0, 0) << "'.\n";
        failedTests++;
    }else{
        passedTests++;
    }
    if(compare_san(0, 0, 0) != 0){
        hwlib::cout << "compare_san(0, 0, 0) failed, expected '0', got '" << compare_san(0, 0, 0) << "'.\n";
        failedTests++;
    }else{
        passedTests++;
    }
    if(compare_san(1, 0, 1) != 1){
        hwlib::cout << "compare_san(1, 0, 1) failed, expected '1', got '" << compare_san(1, 0, 1) << "'.\n";
        failedTests++;
    }else{
        passedTests++;
    }
    if(compare_san(1, 1, 1) != 1){
        hwlib::cout << "compare_san(1, 1, 1) failed, expected '1', got '" << compare_san(1, 1, 1) << "'.\n";
        failedTests++;
    }else{
        passedTests++;
    }
    if(compare_san(0, 1, 1) != 0){
        hwlib::cout << "compare_san(0, 1, 1) failed, expected '0', got '" << compare_san(0, 1, 1) << "'.\n";
        failedTests++;
    }else{
        passedTests++;
    }
    if(compare_san(0, 1, 2) != 1){
        hwlib::cout << "compare_san(0, 1, 2) failed, expected '1', got '" << compare_san(0, 1, 2) << "'.\n";
        failedTests++;
    }else{
        passedTests++;
    }
    if(compare_san(0, 0, 2) != 0){
        hwlib::cout << "compare_san(0, 0, 2) failed, expected '0', got '" << compare_san(0, 0, 2) << "'.\n";
        failedTests++;
    }else{
        passedTests++;
    }
    if(compare_san(0, 1, 3) != 1){
        hwlib::cout << "compare_san(0, 1, 3) failed, expected '1', got '" << compare_san(0, 1, 3) << "'.\n";
        failedTests++;
    }else{
        passedTests++;
    }
    if(compare_san(1, 1, 3) != 1){
        hwlib::cout << "compare_san(1, 1, 3) failed, expected '1', got '" << compare_san(1, 1, 3) << "'.\n";
        failedTests++;
    }else{
        passedTests++;
    }
    if(compare_san(1, 0, 3) != 0){
        hwlib::cout << "compare_san(1, 0, 3) failed, expected '0', got '" << compare_san(1, 0, 3) << "'.\n";
        failedTests++;
    }else{
        passedTests++;
    }
    // Now let's test with negatives
    if(compare_san(0, -1, 0) != 1){
        hwlib::cout << "compare_san(0, -1, 0) failed, expected '1', got '" << compare_san(0, -1, 0) << "'.\n";
        failedTests++;
    }else{
        passedTests++;
    }
    if(compare_san(-1, -1, 0) != 0){
        hwlib::cout << "compare_san(-1, -1, 0) failed, expected '0', got '" << compare_san(-1, -1, 0) << "'.\n";
        failedTests++;
    }else{
        passedTests++;
    }
    if(compare_san(0, -1, 1) != 1){
        hwlib::cout << "compare_san(0, -1, 1) failed, expected '1', got '" << compare_san(0, -1, 1) << "'.\n";
        failedTests++;
    }else{
        passedTests++;
    }
    if(compare_san(-1, -1, 1) != 1){
        hwlib::cout << "compare_san(-1, -1, 1) failed, expected '1', got '" << compare_san(-1, -1, 1) << "'.\n";
        failedTests++;
    }else{
        passedTests++;
    }
    if(compare_san(-1, 0, 1) != 0){
        hwlib::cout << "compare_san(-1, 0, 1) failed, expected '0', got '" << compare_san(-1, 0, 1) << "'.\n";
        failedTests++;
    }else{
        passedTests++;
    }
    if(compare_san(-1, 0, 2) != 1){
        hwlib::cout << "compare_san(-1, 0, 2) failed, expected '1', got '" << compare_san(-1, 0, 2) << "'.\n";
        failedTests++;
    }else{
        passedTests++;
    }
    if(compare_san(-1, -1, 2) != 0){
        hwlib::cout << "compare_san(-1, -1, 2) failed, expected '0', got '" << compare_san(-1, -1, 2) << "'.\n";
        failedTests++;
    }else{
        passedTests++;
    }
    if(compare_san(-1, 0, 3) != 1){
        hwlib::cout << "compare_san(-1, 0, 3) failed, expected '1', got '" << compare_san(-1, 0, 3) << "'.\n";
        failedTests++;
    }else{
        passedTests++;
    }
    if(compare_san(-1, -1, 3) != 1){
        hwlib::cout << "compare_san(-1, -1, 3) failed, expected '1', got '" << compare_san(-1, -1, 3) << "'.\n";
        failedTests++;
    }else{
        passedTests++;
    }
    if(compare_san(0, -1, 3) != 0){
        hwlib::cout << "compare_san(0, -1, 3) failed, expected '0', got '" << compare_san(0, -1, 3) << "'.\n";
        failedTests++;
    }else{
        passedTests++;
    }

    // Mode 4 doesnt exist so we expect a -1.
    if(compare_san(420, 69, 4) != -1){
        hwlib::cout << "compare_san(420, 69, 4) failed, expected '-1', got '" << compare_san(420, 69, 4) << "'.\n";
        failedTests++;
    }else{
        passedTests++;
    }

    // The following test for loops, in their various forms. The modes are:
    // 0. Default starting value of 0, default increment of 1, custom control value, smaller than comparison.
    // 1. Custom starting value, default increment of 1, custom control value, smaller than comparison.
    // 2. Custom starting value, default increment of -1, custom control value, greater than comparison.
    // 3. Custom everything, smaller than comparison.
    // The function increases a counter by 1 every loop and returns that.
    if(forLoop_san(420, 69, 1337, 0) != 1337){
        hwlib::cout << "compare_san(420, 69, 1337, 0) failed, expected '1337', got '" << forLoop_san(420, 69, 1337, 0) << "'.\n";
        failedTests++;
    }else{
        passedTests++;
    }
    if(forLoop_san(337, 69, 1337, 1) != 1000){
        hwlib::cout << "compare_san(337, 69, 1337, 1) failed, expected '1000', got '" << forLoop_san(337, 69, 1337, 1) << "'.\n";
        failedTests++;
    }else{
        passedTests++;
    }
    if(forLoop_san(1337, 69, 337, 2) != 1000){
        hwlib::cout << "compare_san(1337, 69, 337, 2) failed, expected '1000', got '" << forLoop_san(1337, 69, 337, 2) << "'.\n";
        failedTests++;
    }else{
        passedTests++;
    }
    if(forLoop_san(0, 2, 200, 3) != 100){
        hwlib::cout << "compare_san(0, 2, 200, 3) failed, expected '100', got '" << forLoop_san(0, 2, 200, 3) << "'.\n";
        failedTests++;
    }else{
        passedTests++;
    }

    hwlib::cout << "Passed " << passedTests << " tests. Failed " << failedTests << " tests. For a succes rate of " << int(100*(float(passedTests)/float(passedTests+failedTests))) << "%.\n";
}