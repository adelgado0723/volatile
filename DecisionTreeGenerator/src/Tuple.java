/*
 * Authors:
 * 		Arlet Bode   
 * 		Elisa Moral 
 * 		Andres Delgado	
 * 
 * 
 * The Tuple class defines a Tuple and its single member, an array
 * of ints the length of the number of attributes obtained from the
 * input file. Each int in the indexOfDomainValues array maps to
 * a domain value for a provided attribute number, used as the index.
 * 
 */
public class Tuple 
{
	public int[] indexOfDomainValue;

	public Tuple(int attributeCount)
	{
		indexOfDomainValue = new int[attributeCount];

	}
}
