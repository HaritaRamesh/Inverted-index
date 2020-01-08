import sys
import collections
def main(argv):
    f_output=open(argv[2],"w+")

    class linked_list_node:
        def __init__(self,data,freq_term,no_of_terms,no_of_docs,nextnode=None):
            #comprises of the document id
            self.data=data
            self.nextnode=nextnode
            #freq_term = number of time the term has occured in the document
            self.freq_term=freq_term
            #no_of_terms = number of terms in the document
            self.no_of_terms=no_of_terms
            #no_of_docs = Total number of documents in the corpus
            self.no_of_docs=no_of_docs
            #term frequency
            self.term_freq=0.0
            #inverse document frequency
            self.tf_idf=0.0

        def tf(self):
            #Calculating the term frequency
            self.term_freq=self.freq_term/self.no_of_terms
            return self.term_freq

    class linked_list:
        def __init__(self,head=None):
            self.head=None

        #insert function is used to insert the first postings list for a key
        def insert(self,value,freq_term,no_of_terms,no_of_docs):
            node=linked_list_node(value,freq_term,no_of_terms,no_of_docs)
            if self.head is None:
                self.head=node
                return node
            else:
                curr=self.head
                while True:
                    if curr.nextnode is None:
                        curr.nextnode=node
                        break
                    else:
                        curr=curr.nextnode
            return node

        #print the nodes of the postings_list
        def printlink(self):
            curr=self.head
            if curr is None:
                return ""
                #return " "
            while(curr is not None):
                f_output.write(" "+curr.data)
                curr=curr.nextnode
            return ""

        #count the number of nodes of the postings_list
        def count(self):
            count=0
            curr=self.head
            while(curr is not None):
                count=count+1
                curr=curr.nextnode
            return count

        #insert node into an already created postings_list
        def insert1(self,value,freq_term,no_of_terms,no_of_docs):
            node=linked_list_node(value,freq_term,no_of_terms,no_of_docs)
            curr=self.head
            while True:
                if (curr.data==node.data):
                    curr.freq_term=curr.freq_term+1
                    return node
                if curr.nextnode is None:
                    curr.nextnode=node
                    break
                else:
                    curr=curr.nextnode
            return node

    #To calculate the total number of documents in the file
    with open(argv[1], 'r') as f:
        lst=[]
        lst_val=[]
        count_of_docs=0
        for line in f:
            count_of_docs=count_of_docs+1
        f.close()

    #To create a dictionary with the key as the term and the value as the postings_list
    with open(argv[1], 'r') as f:
        d = {}
        for line in f.readlines():
            line = line.split('\t')
            key = line[1].strip()
            line_terms=line[1].split(' ')
            lst.append(len(line_terms))
            key1=key.split(" ")
            value = line[0].strip()
            lst_val.append(value)
            for k in key1:
                if k in d:
                    #if key already exists in dictionary, insert the node to the postings list
                    no_of_docs=count_of_docs
                    x=lst_val.index(str(value))
                    no_of_terms=lst[x]
                    d[k].insert1(value,freq_term,no_of_terms,no_of_docs)
                else:
                    #if key is new, create a new linked list object
                    no_of_docs=count_of_docs
                    x=lst_val.index(str(value))
                    no_of_terms=lst[x]
                    freq_term=1
                    temp = linked_list()
                    temp.insert(value,freq_term,no_of_terms,no_of_docs)
                    d[k] = temp

    #calculating the term frequency for all the document ids
    for key,value in d.items():
        value1=value.head
        while(value1 is not None):
            value1.tf()
            value1=value1.nextnode

    #calculating the inverse document frequency
    for key,value in d.items():
        value1=value.head
        while(value1 is not None):
            no_docs_with_term=value.count()
            idf=value1.no_of_docs/no_docs_with_term
            value1.tf_idf=(value1.term_freq)*idf
            value1=value1.nextnode
    f.close()

    #GetPostings list returns the postings list of the terms
    def GetPostings(term):
        f_output.write("GetPostings\n")
        f_output.write(term)
        f_output.write('\nPostings list:')
        f_output.write(str(d[term].printlink()))
        f_output.write("\n")
        return d[term]


    def GetPostings1(term): #FUNCTION WITHOUT THE F_OUT STATEMENTS
        return d[term]

    #Merge function for the DAAT OR
    def merge(x,y):
        post_lst1=x.head
        post_lst2=y.head
        sorted_lst=linked_list()
        compare=0
        while True:
            if(post_lst1 is not None):
                if(post_lst2 is not None):
                    if(post_lst1.data<post_lst2.data):
                        t=sorted_lst.insert(post_lst1.data,post_lst1.freq_term,post_lst1.no_of_terms,post_lst1.no_of_docs)
                        t.tf_idf=post_lst1.tf_idf
                        compare=compare+1
                        post_lst1=post_lst1.nextnode
                    elif(post_lst2.data<post_lst1.data):
                        t=sorted_lst.insert(post_lst2.data,post_lst2.freq_term,post_lst2.no_of_terms,post_lst2.no_of_docs)
                        t.tf_idf=post_lst2.tf_idf
                        post_lst2=post_lst2.nextnode
                        compare=compare+1
                    elif(post_lst1.data==post_lst2.data):
                        t=sorted_lst.insert(post_lst1.data,post_lst1.freq_term,post_lst1.no_of_terms,post_lst1.no_of_docs)
                        t.tf_idf=post_lst1.tf_idf+post_lst2.tf_idf
                        post_lst1=post_lst1.nextnode
                        post_lst2=post_lst2.nextnode
                        compare=compare+1
                else:
                    break
            else:
                break

        while(post_lst1 is not None):
            t=sorted_lst.insert(post_lst1.data,post_lst1.freq_term,post_lst1.no_of_terms,post_lst1.no_of_docs)
            t.tf_idf=post_lst1.tf_idf
            post_lst1=post_lst1.nextnode

        while(post_lst2 is not None):
            t=sorted_lst.insert(post_lst2.data,post_lst2.freq_term,post_lst2.no_of_terms,post_lst2.no_of_docs)
            t.tf_idf=post_lst2.tf_idf
            post_lst2=post_lst2.nextnode
        return sorted_lst,compare

    #INTERMEDIATE MERGING OF POSTINGS LISTS
    def merge_inter1(lst,compare_lst):
        m=0
        i=0
        w=[]
        compare_lst1=compare_lst[:]
        l=len(lst)
        if(l==1):
            return lst[0]

        if(l==2):
            z,comp=merge(lst[m],lst[m+1])
            compare_lst1.append(comp)
            w.append(z)
        elif(l==3):
            z,comp=merge(lst[m],lst[m+1])
            compare_lst1.append(comp)
            q,comp1=merge(z,lst[m+2])
            compare_lst1.append(comp1)
            w.append(q)
        elif(l>3):
            if l%2==0:
                while(m<=l-2):
                    z,comp=merge(lst[m],lst[m+1])
                    compare_lst.append(comp)
                    w.append(z)
                    m=m+2
            else:
                while(m<=l-2):
                    z,comp=merge(lst[m],lst[m+1])
                    compare_lst.append(comp)
                    w.append(z)
                    m=m+2
                w.append(lst[l-1])

        return merge_inter1(w,compare_lst1)

    #DAAT_OR FUNCTION
    def DAAT_or(list_of_words):
        f_output.write("DaatOr\n")
        lst=[]
        f_output.write(str(" ".join(list_of_words)))
        f_output.write("\n")
        for word in list_of_words:
            x=GetPostings1(word)
            lst.append(x)
        l=len(list_of_words)
        m=0
        i=0
        w=[]
        compare_lst=[]
        if(l==2):
            f1,comp=merge(lst[m],lst[m+1])
            compare_lst.append(comp)
        elif(l==3):
            z,comp=merge(lst[m],lst[m+1])
            compare_lst.append(comp)
            q,comp1=merge(z,lst[m+2])
            compare_lst.append(comp1)
            f1=q
        elif(l>3):
            if l%2==0:
                while(m<=l-2):
                    z,comp=merge(lst[m],lst[m+1])
                    w.append(z)
                    compare_lst.append(comp)
                    m=m+2
                f1,compare_lst=merge_inter1(w,compare_lst)
            else:
                while(m<=l-2):
                    z,comp=merge(lst[m],lst[m+1])
                    w.append(z)
                    compare_lst.append(comp)
                    m=m+2
                w.append(lst[l-1])
                f1,compare_lst=merge_inter1(w,compare_lst)

        comparisons=sum(compare_lst)
        number_of_nodes=f1.count()
        if(number_of_nodes==0):
            f_output.write("Results: empty\n")
            f_output.write("Number of documents in results: ")
            f_output.write(str(f1.count()))
            f_output.write("\n")
            f_output.write("Number of comparisons: ")
            f_output.write(str(comparisons))
            f_output.write("\n")
        else:

            f_output.write("Results:")
            f_output.write(str(f1.printlink()))
            f_output.write("\n")
            f_output.write("Number of documents in results: ")
            f_output.write(str(f1.count()))
            f_output.write("\n")
            f_output.write("Number of comparisons: ")
            f_output.write(str(comparisons))
            f_output.write("\n")
        return f1

    #MERGE FUNCTION FOR DAAT AND
    def merge1(x,y):
        post_lst1=x.head
        post_lst2=y.head
        sorted_lst=linked_list()
        compare=0
        while True:
            if(post_lst1 is not None):
                if(post_lst2 is not None):
                    if(post_lst1.data<post_lst2.data):
                        compare=compare+1
                        post_lst1=post_lst1.nextnode
                    elif(post_lst2.data<post_lst1.data):
                        post_lst2=post_lst2.nextnode
                        compare=compare+1
                    elif(post_lst1.data==post_lst2.data):
                        t=sorted_lst.insert(post_lst1.data,post_lst1.freq_term,post_lst1.no_of_terms,post_lst1.no_of_docs)
                        t.tf_idf=post_lst1.tf_idf+post_lst2.tf_idf
                        post_lst1=post_lst1.nextnode
                        post_lst2=post_lst2.nextnode
                        compare=compare+1
                else:
                    break
            else:
                break
        return sorted_lst,compare

    #INTERMEDIATE MERGE OPERATION FOR DAAT- AND
    def merge_inter_and(lst,compare_lst):
        m=0
        i=0
        w=[]
        compare_lst1=compare_lst[:]
        l=len(lst)
        if(l==1):
            return lst[0],compare_lst1
        if(l==2):
            z,comp=merge1(lst[m],lst[m+1])
            compare_lst1.append(comp)
            w.append(z)
        elif(l==3):
            z,comp=merge1(lst[m],lst[m+1])
            compare_lst1.append(comp)
            q,comp1=merge1(z,lst[m+2])
            compare_lst1.append(comp1)
            w.append(q)
        elif(l>3):
            if l%2==0:
                while(m<=l-2):
                    z,comp=merge1(lst[m],lst[m+1])
                    compare_lst1.append(comp)
                    w.append(z)
                    m=m+2
            else:
                while(m<=l-2):
                    z,comp=merge1(lst[m],lst[m+1])
                    compare_lst1.append(comp)
                    w.append(z)
                    m=m+2
                w.append(lst[l-1])
        return merge_inter_and(w,compare_lst1)

    #DAAT-AND FUNCTION
    def DAAT_and(list_of_words):
        f_output.write("DaatAnd\n")
        lst=[]
        compare_lst=[]
        f_output.write(str(" ".join(list_of_words)))
        f_output.write("\n")
        for word in list_of_words:
            x=GetPostings1(word)
            lst.append(x)
        l=len(list_of_words)
        m=0
        i=0
        w=[]
        if(l==2):
            f1,comp=merge1(lst[m],lst[m+1])
            compare_lst.append(comp)
        elif(l==3):
            z,comp=merge1(lst[m],lst[m+1])
            compare_lst.append(comp)
            q,comp1=merge1(z,lst[m+2])
            compare_lst.append(comp1)
            f1=q
        elif(l>3):
            if l%2==0:
                while(m<=l-2):
                    z,comp=merge1(lst[m],lst[m+1])
                    w.append(z)
                    compare_lst.append(comp)
                    m=m+2
                f1=merge_inter_and(w,compare_lst)
            else:
                while(m<=l-2):
                    z,comp=merge1(lst[m],lst[m+1])
                    compare_lst.append(comp)
                    w.append(z)
                    m=m+2
                w.append(lst[l-1])
                f1=merge_inter_and(w,compare_lst)
        comparisons=sum(compare_lst)
        number_of_nodes=f1.count()
        if(number_of_nodes==0):
            f_output.write("Results: empty\n")
            f_output.write("Number of documents in results: ")
            f_output.write(str(f1.count()))
            f_output.write("\n")
            f_output.write("Number of comparisons: ")
            f_output.write(str(comparisons))
            f_output.write("\n")
        else:
            f_output.write("Results:")
            f_output.write(str(f1.printlink()))
            f_output.write("\n")
            f_output.write("Number of documents in results: ")
            f_output.write(str(f1.count()))
            f_output.write("\n")
            f_output.write("Number of comparisons: ")
            f_output.write(str(comparisons))
            f_output.write("\n")
        return f1

    def DAAT_and1(list_of_words):
        lst=[]
        for word in list_of_words:
            x=GetPostings1(word)
            lst.append(x)
        l=len(list_of_words)
        m=0
        i=0
        w=[]
        compare_lst=[]
        if(l==2):
            f1,comp=merge1(lst[m],lst[m+1])
            compare_lst.append(comp)
        elif(l==3):
            z,comp=merge1(lst[m],lst[m+1])
            compare_lst.append(comp)
            q,comp1=merge1(z,lst[m+2])
            compare_lst.append(comp1)
            f1=q
        elif(l>3):
            if l%2==0:
                while(m<=l-2):
                    z=merge1(lst[m],lst[m+1])
                    w.append(z)
                    compare_lst.append(comp1)
                    m=m+2
                f1=merge_inter_and(w,compare_lst)
            else:
                while(m<=l-2):
                    z=merge1(lst[m],lst[m+1])
                    w.append(z)
                    compare_lst.append(comp1)
                    m=m+2
                w.append(lst[l-1])
                f1=merge_inter_and(w,compare_lst)
        return f1

    def DAAT_or1(list_of_words):
        lst=[]
        for word in list_of_words:
            x=GetPostings1(word)
            lst.append(x)
        l=len(list_of_words)
        m=0
        i=0
        w=[]
        compare_lst=[]
        if(l==2):
            f1,comp=merge(lst[m],lst[m+1])
            compare_lst.append(comp)
        elif(l==3):
            z,comp=merge(lst[m],lst[m+1])
            compare_lst.append(comp)
            q,comp1=merge(z,lst[m+2])
            compare_lst.append(comp1)
            f1=q
        elif(l>3):
            if l%2==0:
                while(m<=l-2):
                    z,comp=merge(lst[m],lst[m+1])
                    w.append(z)
                    compare_lst.append(comp)
                    m=m+2
                f1,compare_lst=merge_inter1(w,compare_lst)
            else:
                while(m<=l-2):
                    z,comp=merge(lst[m],lst[m+1])
                    w.append(z)
                    compare_lst.append(comp)
                    m=m+2
                w.append(lst[l-1])
                f1,compare_lst=merge_inter1(w,compare_lst)
        return f1

    #SORTED LIST WITH RESPECT TO TF-IDF
    def sort1(f):
        f_output.write("TF-IDF\n")
        d_sort={}
        value1=f.head
        key1=[]
        val=[]
        while(value1 is not None):
            key1.append(value1.tf_idf)
            val.append(value1.data)
            value1=value1.nextnode
        i=0
        for v in val:
            d_sort[v]=key1[i]
            i=i+1
        x=sorted(d_sort.items(),key=lambda kv: kv[1],reverse=True)
        result=[]
        for a,b in x:
            result.append(a)
        if (len(result)==0):
            f_output.write("Results: empty\n")
        else:
            f_output.write("Results: ")
            f_output.write(str(" ".join(result)))
            f_output.write("\n")
            #f_output.write("")
        return result

    #Reading the input using commandline arguments
    with open(argv[3],'r') as file:
        newline = ''
        for line in file.readlines():
            line = line.strip()
            words=line.split(" ")
            f_output.write(newline)
            for word in words:
                #step 1 : Get postings lists
                GetPostings(word)
            newline='\n'
            #step 2 : DAAT - AND for the query terms
            DAAT_and(words)
            #step 3: DAAT - AND in sorted tf-idf order
            sort1(DAAT_and1(words))
            #step 4: DAAT - OR for the query terms
            DAAT_or(words)
            #step 5: DAAT - OR in sorted tf-idf order
            sort1(DAAT_or1(words))
            #f_output.write("\n")
    file.close()

if __name__ == "__main__":
    main(sys.argv)
