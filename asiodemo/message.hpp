#ifndef MESSAGE_H
#define MESSAGE_H
#include <cstdlib>
#include <cstring>
#include <cstdio>
#include <string>

class message{
public:
    enum {header_length = 4};
    enum {max_body_length = 128};

    message():body_length_(0){
        memset(data_,'\0', header_length+max_body_length);
    }
    message(const std::string &msg){
        body_length(msg.size());
        memcpy(body(), msg.c_str(), body_length());
        encode_header();
    }

    message(const char* msg){
        body_length(strlen(msg));
        memcpy(body(), msg, body_length());
        encode_header();
    }

    void clear(){
        memset(data_, '\0', length());
        body_length_ = 0;
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
    void body_length(size_t bdlen){
        body_length_ = bdlen;
    }

    void encode_header(){
        using namespace std;
        char header[header_length+1]="";
        sprintf(header,"%4lu",body_length_);
        memcpy(data_, header, header_length);
    }
    bool decode_header(){
        using namespace std;
        char header[header_length+1] = "";
        strncat(header, data_, header_length);
        body_length_ = atoi(header);
        if (body_length_ > max_body_length){
            body_length_ = 0;
            return false;
        }
        return true;
    }

private:
    char data_[header_length+max_body_length];
    size_t body_length_;
};

#endif
