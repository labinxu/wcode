https://linux.cn/article-8498-1.html
//
poor taste
remove_list_entry(entry)
{
prev = NULL;
walk = head;
// Walk the list
while(walk != entry){
prev = walk;
walk = walk->next;
}
// Remove the entry by updating the head or the previous entry
if(!prev){
head = entry->next;
}
else{
prev->next = entr->next;
}

}

// good taste
remove_list_entr(entry){
  // The indirect pointer points to the address of the thing we'll update
  indirect = &head;
  // Walk the list looking for the thing that
  // points to the entr we want to remove
  while((*indirect)!= entry){
    indirect = &(*indirect)->next;
  } 
  // and just remove it
  *indirect = entry->next;
}
////////////////////////////////
for (r = 0; r < GRID_SIZE; ++r) {
    for (c = 0; c < GRID_SIZE; ++c) {
        // Top Edge
        if (r == 0)
            grid[r][c] = 0;
        // Left Edge
        if (c == 0)
            grid[r][c] = 0;
        // Right Edge
        if (c == GRID_SIZE - 1)
            grid[r][c] = 0;
        // Bottom Edge
        if (r == GRID_SIZE - 1)
            grid[r][c] = 0;
    }
}
///
#include <iostream>

using namespace std;
typedef struct node{
	node(int v):data(v),next(NULL){};
	int data;
	node *next;
} node;
class List{
	private:
		node *head;
	public:
	List():head(NULL){}
	void push_back(int v){
		cout<<"push_back:"<<v<<endl;
		if(!head){
			head = new node(v);
			return;
		}
		
		node *tmp = head;
		while(tmp->next){
			tmp = tmp->next;
		}
		tmp->next = new node(v);
	};
	void push_back_v2(int v){
		
		if(!head){
			head = new node(v);
			return;
		}
		
		node *tmp = head;
		while(tmp){
			tmp = tmp->next;
		}
		tmp = new node(v);
	};
	public:
	void display(){
		cout<<"display()"<<endl;
		node *tmp=head;
		while(tmp){
			cout<<tmp->data<<";";
			tmp = tmp->next;
		};
		cout<<endl;
	};
	void remove_bad(int entry){
		node* prev = NULL;
		node* walk = head;
		while(walk->data != entry){
			prev = walk;
			walk = walk->next;
		}

		if(!prev){
			head = walk->next;
		}
		else{
			prev->next = walk->next;
		};
	};

	void remove_good(int entry){
		node** indirect = &head;
		while((*indirect)->data != entry){
			indirect = &(*indirect)->next;
		}
	
		// remove
		*indirect = (*indirect)->next;
	}
};
int main() {
	cout << "hello https://tool.lu/" << endl;
	List lst;
	for(int i=0;i<10;i++){
		lst.push_back(i);
	};
	lst.display();
	node n(0);
	//lst.remove_bad(2);
	//lst.display();
	lst.remove_good(10);
	lst.display();
	
	return 0;
}
