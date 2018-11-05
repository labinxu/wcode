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
