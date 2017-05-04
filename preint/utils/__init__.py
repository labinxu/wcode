def sortBuildName(tag1, tag2):
    #tag1 = 'ICE7360_05.1719.05'
    #tag2 = 'ICE7360_05.1719.01'
    tag_1 = tag1.split('.') 
    tag_2 = tag2.split('.')
    for i in range(1, len(tag_1)):
        if int(tag_1[i]) > int(tag_2[i]):
            return tag2, tag1
    return tag1, tag2
