from avl import AVLTree
from avl import GenAVLTree

genome = GenAVLTree()
#genome.put('chr1',12,'a')
#print genome.chroms
genome['chr1'][12] = 'a'
genome['chr2'][13] = 'b'
genome['chr1'][10] = 'a'
genome['chr3'][564880]='c'
genome['chr3'][564881]='d'
genome['chr3'][564882]='e'
genome['chr3'][564883]='f'
genome['chr3'][564884]='fg'
genome['chr3'][564885]='g'
genome['chr3'][564886]='h'
genome['chr3'][564887]='i'
genome['chr3'][564888]='j'

#genome.test()
#print str(tree)
#genome.print_genome()
#print genome['chr3'][564884:564887]
genome.delete('chr2',13)
#genome['chr2'].delete(13)
genome.print_genome()

