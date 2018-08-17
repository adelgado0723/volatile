/*
 * Authors:
 * 		Arlet Bode   
 * 		Elisa Moral 
 * 		Andres Delgado	
 * 
 * The DecisionTreeNode class defines a DecisionTreeNode, its members,
 * and a constructor that initializes them. 
 */

import java.util.Vector;


public class DecisionTreeNode 
{

	public int nodeDomainIndex;
	public int splittingAttributeIndex;
	public Vector data;
	public DecisionTreeNode[] children;
	public DecisionTreeNode parent;
	public double informationGain;


	public DecisionTreeNode()
	{
		nodeDomainIndex = 0;
		splittingAttributeIndex = 0;
		data = new Vector();
		children = null;
		informationGain = 0;
	}
}
