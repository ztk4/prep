//Bucket Sort (for 4 Byte integers ONLY)
#include <inttypes.h>
#include <iterator>
#include <vector>
#include <type_traits>
#include <cstdlib>
#include <ctime>
#include <iostream>

using std::iterator_traits;
using std::random_access_iterator_tag;
using std::vector;
using std::is_same;
using std::endl;
using std::cout;
using std::ostream;

//I must be a random access iterator
template<class I>
void sort(I s, I e) {
	typedef iterator_traits<I> I_traits;
	typedef typename I_traits::value_type T;
	if(!is_same<uint32_t, T>::value) return; //make sure it's a non-negative 4 byte int
	if(!is_same<random_access_iterator_tag, typename I_traits::iterator_category>::value) return; //make sure it's a random access iterator
	vector<T> buckets(0x10001), temp(e-s);
	I p;
	typename vector<T>::iterator t;
	for(p = s; p != e; ++p) //count frequency
		++buckets[1 + (*p & 0xFFFF)];
	for(t = buckets.begin() + 1; t != buckets.end(); ++t) //make list of indexes
		*t += *(t-1);
	for(p = s; p != e; ++p) //sort once
		temp[buckets[*p & 0xFFFF]++] = *p;

	for (t = buckets.begin(); t != buckets.end(); ++t)
		*t = 0;

	for(p = temp.begin(); p != temp.end(); ++p)
		++buckets[1 + ((*p>>16) & 0xFFFF)];
	for(t = buckets.begin() + 1; t != buckets.end(); ++t)
		*t += *(t-1);
	for(p = temp.begin(); p != temp.end(); ++p)
		s[buckets[(*p>>16) & 0xFFFF]++] = *p; //this line requires random access iterator		
}

template<class T>
ostream &operator<<(ostream &o, const vector<T> &v) {
	o << "[\n";
	for(typename vector<T>::const_iterator i = v.begin(); i != v.end()-1; ++i)
		o << ' ' << *i << ", \n";
	return o << ' ' << *(v.end()-1) << "\n]";
}

int main(int argc, char **argv) {
	srand(time(NULL));
	uint32_t size = atoi(*(argv+1));
	vector<uint32_t> test(size);
	for(typename vector<uint32_t>::iterator i = test.begin(); i != test.end(); ++i)
		*i = rand() % 0x100000000 + 1;
	cout << test << endl;
	sort(test.begin(), test.end());
	cout << test << endl;
	return 0;
}
