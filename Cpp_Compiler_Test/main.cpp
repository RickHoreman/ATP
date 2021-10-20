#include "hwlib.hpp"
#include <charconv>

extern "C" void uart_put_int( int n ){
    char n_char[63 + sizeof(char)];
    std::to_chars(n_char, n_char + 63, n);
    hwlib::cout << n_char;
}
extern "C" int sadge_san( int n );


int main(){	
    hwlib::wait_ms(1000);
    hwlib::cout << "Go!\n";
    uart_put_int(sadge_san( 10 ));
    hwlib::cout << "\nDone.";
}