/*
 * Authors:
 * 		Arlet Bode 
 * 		Elisa Moral  
 * 		Andres Delgado	
 *						
 *
 * The DecisionTree class provides functions for reading the provided data,
 * building the decision tree using information gain as the attribute selection
 * method, and printing the tree to a file in the current directory called, 
 * tree.txt. Methods also exist for prompting the user to enter a single record
 * without the class information of the rightmost attribute and then classifying 
 * that record.
 * 
 * The vector attributeDomains has size() equal to the number of attributes that
 * were provided in the input file. For each attribute, it holds a list of all
 * the possible domain values of that attribute. Tuple record values are mapped to this
 * structure in the function parseInput().
 */

import java.awt.HeadlessException;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.util.StringTokenizer;
import java.util.Vector;

import javax.swing.JFileChooser;
import javax.swing.JOptionPane;

public class DecisionTree 
{

	String[] attributeNames;
	Vector[] attributeDomains;
	int totalAttributes = 0;
	DecisionTreeNode root = new DecisionTreeNode();
	FileWriter writer;
	PrintWriter out;

	public DecisionTree()
	{

		try
		{
			writer = new FileWriter("tree.txt");
			out = new PrintWriter(writer);
		}
		catch (IOException e) 
		{
			JOptionPane.showMessageDialog(null, e.toString(), "Problem opening a file for output.", JOptionPane.ERROR_MESSAGE);
		}
	}

	/*
	 * gatherClassOfValueIndex() gathers all of the members of the given tuples that share the 
	 * given valueIndex for the attribute at the given attribute index. This is useful when 
	 * splitting the data based on the tuples values for a specific attribute. 
	 * 
	 */
	public Vector gatherClassOfValueIndex(int valueIndex, int attributeIndex, Vector tuples)
	{
		Vector classOfValueIndex = new Vector();
		int i, numTuples;

		if(tuples != null)
		{
			numTuples = tuples.size();

			for(i = 0; i < numTuples; i++)
			{
				if(((Tuple) tuples.elementAt(i)).indexOfDomainValue[attributeIndex] == valueIndex)
				{
					classOfValueIndex.addElement((Tuple) tuples.elementAt(i));
				}
			}
		}
		return classOfValueIndex;
	}

	/*
	 * getDomainIndex() retrieves the index of a specific domain value for the 
	 * given attributeIndex. It is used in the mapping process of parseInput().
	 * First it checks if the domain value already exists in attribueDomains[].
	 * If so, it returns the index of that value at attributeIndex. That is,
	 * attributeDomains[attributeIndex].indexOf(value). Otherwise, it adds
	 * the value to the attributeDomains vector and returns its index.
	 * 
	 */
	public int getDomainIndex(String value, int attributeIndex)
	{
		if(attributeDomains[attributeIndex].contains(value))
		{
			return attributeDomains[attributeIndex].indexOf(value);

		}
		else 
		{
			attributeDomains[attributeIndex].addElement(value);
			return  attributeDomains[attributeIndex].indexOf(value);
		}
	}

	/*
	 * parseInput() uses a graphical file chooser to have the user open the 
	 * input file. Then it proceeds to read the attribute names and values so 
	 * that it can populate the attributeDomains vector and the attributeNames string 
	 * array. Then, for each tuple and each attribute, the algorithm maps the data 
	 * point's value to the attributeDomains vector. Finally, all records are added
	 * to the data member of the root node.
	 */
	public boolean parseInput()
	{
		// Using a JFileChooser to allow the user to open the input file. 

		File file = null;
		FileInputStream input = null;

		JOptionPane.showMessageDialog(null, "Please select the input file...\n");
		JFileChooser choose = new JFileChooser(".");
		int status = choose.showOpenDialog(null);

		try
		{
			if (status != JFileChooser.APPROVE_OPTION)
			{
				throw new IOException();
			}

			file = choose.getSelectedFile();

			if (!file.exists())
			{
				throw new FileNotFoundException();
			}

			input = new FileInputStream(file.getAbsolutePath());
		}
		catch (NullPointerException e)
		{
			JOptionPane.showMessageDialog(null, e.toString(), "Error", JOptionPane.ERROR_MESSAGE);
			return false;
		}
		catch (FileNotFoundException e) 
		{
			JOptionPane.showMessageDialog(null, e.toString(), "File not found ....", JOptionPane.ERROR_MESSAGE);
			return false;
		} 
		catch (IOException e) 
		{
			JOptionPane.showMessageDialog(null, e.toString(), "Approve option was not selected", JOptionPane.ERROR_MESSAGE);
			return false;
		}


		// Reading the first non-empty line of the input file.
		// It should contain the attribute names separated by a single space.


		// Reading from file into tmp string.

		BufferedReader reader = new BufferedReader(new InputStreamReader(input));

		String tmp = "";

		while(tmp.equals(""))
		{
			try
			{
				tmp = reader.readLine();

			}
			catch(IOException e)
			{
				JOptionPane.showMessageDialog(null, e.toString(), "Error reading attribute names.", JOptionPane.ERROR_MESSAGE);
			}
		}

		StringTokenizer tokenizer = new StringTokenizer(tmp);
		totalAttributes = tokenizer.countTokens();


		// Expecting at least two attributes for calculating information
		// gain and having a meaningful result.
		if(totalAttributes < 2)
		{
			JOptionPane.showMessageDialog(null, "Expecting at least two attributes.", "Error", JOptionPane.ERROR_MESSAGE);
			return false;
		}


		// Initializing each index of the attributeDomains vector with a 
		// vector of its own, creating a 2d vector. Also capturing the 
		// attribute names into the attributeNames[] string array.

		attributeDomains = new Vector[totalAttributes];
		attributeNames = new String[totalAttributes];
		int i;

		for (i = 0; i < totalAttributes; i++)
		{
			attributeNames[i] = tokenizer.nextToken();
			attributeDomains[i] = new Vector();
		}

		// Reading attribute values and assigning them an index that points to 
		// that attribute's domain value in the attributeDomains vector.
		tmp = "";
		try
		{

			while(true)
			{
				tmp = reader.readLine();

				if(!(tmp.equals(null)) && !(tmp.equals("")) ) 
				{
					tokenizer = new StringTokenizer(tmp);

					// Expecting the same number of attributes as specified in the header.
					int attributeCount = tokenizer.countTokens();
					if(totalAttributes != attributeCount)
					{
						JOptionPane.showMessageDialog(null, "Expecting the same number of attributes for each tuple as specified in the header. found:" + attributeCount
								+"\n On iteration: " + (root.data.size()-1), "Error", JOptionPane.ERROR_MESSAGE);
						return false;
					}

					Tuple t = new Tuple(totalAttributes);
					int j;
					for(j = 0; j < totalAttributes; j++)
					{
						t.indexOfDomainValue[j] = getDomainIndex(tokenizer.nextToken(), j);
					}

					// Adding every record to the root of the tree to start off.
					root.data.addElement(t);

				}
			}

		}
		catch(IOException e)
		{
			JOptionPane.showMessageDialog(null, e.toString(), "Error reading attribute names.", JOptionPane.ERROR_MESSAGE);
		}
		catch(NullPointerException e){}

		try 
		{
			reader.close();
		} 
		catch (IOException e) 
		{
			JOptionPane.showMessageDialog(null, "Error closing reader.", "IOERROR", JOptionPane.ERROR_MESSAGE);
		}

		return true;
	}

	/*
	 * readAndClassifyTuple() reads a single tuple from the console,
	 * translates its values to indeces that poing to the attributeDomains
	 * vector, and then calls the helper function, to classifyTuple() guess
	 * the class label of the provided tuple.
	 * 
	 */
	public boolean readAndClassifyTuple() 
	{


		// Reading a single tuple from the console.
		String in = null;
		try
		{
			in = JOptionPane.showInputDialog("Enter the values, for the tuple to be classified, separated by a single space.");
		}
		catch(HeadlessException e)
		{
			JOptionPane.showMessageDialog(null, "Error reading tuple from JOptionPane.", "Headless Exception", JOptionPane.ERROR_MESSAGE);
		}

		if(in == null || in.equals(""))
		{
			JOptionPane.showMessageDialog(null, "No input provided. Please run program again.", "IOERROR", JOptionPane.ERROR_MESSAGE);
			return false;
		}

		StringTokenizer tokenizer = new StringTokenizer(in);

		int tokens = tokenizer.countTokens();

		// totalAttributes - 1 since there is a missing attribute that will be assigned.
		if(tokens != (totalAttributes - 1))
		{
			JOptionPane.showMessageDialog(null, "Expecting " + (totalAttributes - 1) + " number of values. Please run program again.\n", "IOERROR", JOptionPane.ERROR_MESSAGE);
			return false;
		}

		Tuple tuple = new Tuple(totalAttributes);

		// Populating the tuple's attribute array
		int i;
		for(i = 0; i < (totalAttributes - 1); i++){

			tuple.indexOfDomainValue[i] = getDomainIndex(tokenizer.nextToken(), i);
		}



		// Classifying the given tuple:
		classifyTuple(tuple, root);

		JOptionPane.showMessageDialog(null,"The given tuple belongs in the class of:\n"
				+ (String) attributeDomains[totalAttributes - 1].elementAt(tuple.indexOfDomainValue[totalAttributes - 1]) 
				+ "\nFor the attribute:\n" + attributeNames[totalAttributes - 1]);

		return true;



	}
	/*
	 * classifyTuple() is a helper function that recursively traverses the tree
	 * looking for the class that the input tuple belongs to.
	 * 
	 */
	public void classifyTuple(Tuple tuple, DecisionTreeNode node)
	{


		if(node.children == null )
		{
			tuple.indexOfDomainValue[totalAttributes - 1] = ((Tuple)node.data.elementAt(0)).indexOfDomainValue[totalAttributes - 1];	
			return;
		}

		else
		{
			classifyTuple(tuple, node.children[tuple.indexOfDomainValue[node.splittingAttributeIndex]]);
		}
	}


	/*
	 * graphTree() writes a graphical to the text file, tree.txt. It cycles recursively
	 * through all the children of the tree and printing the records associated with each 
	 * leaf node.
	 * 
	 */
	public void graphTree(DecisionTreeNode node, String tabs)
	{
		int classifyingAttribute = totalAttributes - 1;

		if(node.parent == null)
		{
			out.println("Decision Tree Using Information Gain to Select The Splitting Attribute\n\n");
			out.println("The root attribute is:\n" + attributeNames[node.splittingAttributeIndex] + "\n\n");

		}
		if(node.children == null)
		{	
			// Retrieving the domain of the classifying attribute from the 
			// node.data field
			Vector tmpVector = new Vector();

			int numTuples = node.data.size();
			int i;
			for (i = 0; i < numTuples; i++) 
			{
				Tuple tuple = (Tuple) node.data.elementAt(i);

				String symbol
					= (String) attributeDomains[classifyingAttribute].elementAt(tuple.indexOfDomainValue[classifyingAttribute]);

				if (!tmpVector.contains(symbol)) 
				{
					tmpVector.addElement(symbol);
				}
			}//end of for loop

			int[] domainOfClassifyingAttribute = new int[tmpVector.size()];

			for (i = 0; i < domainOfClassifyingAttribute.length; i++) 
			{
				String symbol = (String) tmpVector.elementAt(i);
				domainOfClassifyingAttribute[i] = attributeDomains[classifyingAttribute].indexOf(symbol);
			}

			tmpVector = null;

			if (domainOfClassifyingAttribute.length == 1) 
			{

				out.println(tabs + "\t" + attributeNames[classifyingAttribute] + " = "
						+ attributeDomains[classifyingAttribute].elementAt(domainOfClassifyingAttribute[0]) ) ;

				out.println("\n" + tabs + "\tRECORDS:\n"+printTuples(gatherClassOfValueIndex(domainOfClassifyingAttribute[0], classifyingAttribute, node.data), tabs + "\t"));

			}
			else
			{
				out.print(tabs + "\t" + attributeNames[classifyingAttribute] + " = ");

				for (i = 0; i < domainOfClassifyingAttribute.length; i++) 
				{
					out.print(attributeDomains[classifyingAttribute].elementAt(domainOfClassifyingAttribute[i]));

					if (i != domainOfClassifyingAttribute.length - 1) 
					{
						out.print(" OR ");
					}
				}
				for (i = 0; i < domainOfClassifyingAttribute.length; i++)
				{
					out.print("\n" + tabs + "\tRECORDS:\n"+printTuples(gatherClassOfValueIndex(domainOfClassifyingAttribute[i], classifyingAttribute, node.data), tabs + "\t") +"\n");	
				}
			}

		}
		else
		{
			int numChildren = node.children.length;
			int i;
			for (i = 0; i < numChildren; i++) {

				out.println(tabs + "IF "  + attributeNames[node.splittingAttributeIndex] + " == " 
						+ attributeDomains[node.splittingAttributeIndex].elementAt(i) );

				//String paritialOutput = "";
				graphTree(node.children[i], tabs + "\t");
			}
		}


	}

	public String printTuples(Vector tuples, String tabs)
	{
		String out = new String("");
		int numTuples = tuples.size();
		int i;
		for(i = 0; i < numTuples; i++)
		{

			int  numDomainValues = ((Tuple) tuples.elementAt(i)).indexOfDomainValue.length;
			out += tabs;
			int j;
			for(j = 0; j < numDomainValues; j++)
			{
				out += (String) attributeDomains[j].elementAt(((Tuple) tuples.elementAt(i)).indexOfDomainValue[j]) + " "; 
			}
			out += "\n";
		}

		return out;
	}


	/*
	 * buildTree() takes the data collected at the root node of the decision tree in
	 * parseInput() and splits it based on a single attribute, using information gain
	 * as the attribute selection method. This method uses formulas 8.1, 8.2, and 8.3
	 * from the textbook to calculate the information gain of each attribute at each 
	 * node of the tree.
	 * 
	 */
	public void buildTree(DecisionTreeNode node)
	{
		double highestInformationGain = -1;
		int splittingAttributeIndex  = -1;
		int numTuples = node.data.size();
		node.informationGain = getEntropy(node.data);

		if(node.informationGain <= 0)
		{
			return;
		}
		else
		{
			int i;
			for (i = 0; i < totalAttributes - 1; i++) 
			{

				int numDomainValues = attributeDomains[i].size();

				if (!wasSplittingAttribute(node, i)) 
				{
					double attributeEntropy = 0;
					int j;	
					for (j = 0; j < numDomainValues; j++) 
					{
						Vector classOfJInI = gatherClassOfValueIndex(j, i, node.data);

						if (classOfJInI.size() > 0) 
						{
							attributeEntropy += getEntropy(classOfJInI) * classOfJInI.size()/numTuples;
						}
					}
					attributeEntropy = node.informationGain - attributeEntropy;


					if (attributeEntropy > highestInformationGain) 
					{
						highestInformationGain = attributeEntropy;
						splittingAttributeIndex = i;
					}
				}
			}
			if(splittingAttributeIndex != -1)
			{


				int splittingAttributeDomain = attributeDomains[splittingAttributeIndex].size();

				node.splittingAttributeIndex = splittingAttributeIndex;

				node.children = new DecisionTreeNode[splittingAttributeDomain];

				for (i = 0; i < splittingAttributeDomain; i++) 
				{
					node.children[i] = new DecisionTreeNode();
					node.children[i].parent = node;
					node.children[i].nodeDomainIndex = i;
					node.children[i].data = gatherClassOfValueIndex(i, splittingAttributeIndex, node.data);

					buildTree(node.children[i]);

				}
			}


			node.data = null;
			return;
		}
	}

	/*
	 * getEntropy() performs the basic entropy calculation on a set of tuples.
	 * It follows formula 8.1 from the textbook.
	 * 
	 */
	public double getEntropy(Vector tuples)
	{
		int numTuples = tuples.size();

		if(numTuples > 0)
		{
			double partialSum = 0;
			int classifyingAttributeDomain = attributeDomains[totalAttributes - 1].size();
			int i;
			for(i = 0; i < classifyingAttributeDomain; i++)
			{
				// Count will keep track of the number of attributes that
				// have domain value j for tuple i
				int attributesInClassI = 0;
				int j;
				for(j = 0; j < numTuples; j++)
				{
					Tuple t = (Tuple) tuples.elementAt(j);

					if(t.indexOfDomainValue[totalAttributes - 1] == i)
					{
						attributesInClassI++;
					}
				}
				double probabilityOfClassI = (double) attributesInClassI / numTuples;

				// Converting from natural logarithm to base 2
				if(probabilityOfClassI != 0)
				{
					partialSum += -(probabilityOfClassI * (Math.log(probabilityOfClassI)/Math.log(2)));
				}
			}
			return partialSum;
		}
		else
		{
			return 0;
		}

	}

	/*
	 * wasSplittingAttribute() recursively checks if any of the ancestor nodes of the
	 * parameter node has the attribute in question as its splittingAttribute. If the 
	 * function makes it all the way up to the root without returning true at some node,
	 * then it can return false, meaning that the attribute in question has not yet been 
	 * used to split this branch of the tree. 
	 * 
	 */
	public boolean wasSplittingAttribute(DecisionTreeNode node, int attributeIndex)
	{
		if (node.children != null && node.splittingAttributeIndex == attributeIndex) 
		{
			return true;
		}
		if(node.parent == null)
		{
			return false;
		}
		return wasSplittingAttribute(node.parent, attributeIndex);
	}

}
