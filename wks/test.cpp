class Base{
public:
  virtual void foo(){};
};
class Drived: public Base{
public:
  virtual void foo(){};
};
int main(){
  Base *bp = new Drived();
  bp->foo();
	return 0;
}
