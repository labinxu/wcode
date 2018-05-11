#ifndef MESSAGE_H
#define MESSAGE_H
#include <cstdlib>
#include <cstring>
#include <cstdio>

class message{
public:
    enum {header_length = 4};
    enum {max_body_length = 128};

    message():body_length_(0){
        //memset()
    }
    char *data(){return data_;}
    const char* data() const {return data_;}
    size_t length() const{
        return header_length + body_length_;
    }
    const char* body() const{
        return data_ + header_length;
    }
    char *body() {return data_ + header_length;}
    size_t body_length() const{ return body_length_;}

private:
    char data_[header_length+max_body_length];
    size_t body_length_;
};

#endif
