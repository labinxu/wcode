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
