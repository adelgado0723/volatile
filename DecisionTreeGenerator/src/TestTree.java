/*
 * Authors:
 * 		Arlet Bode   
 * 		Elisa Moral 
 * 		Andres Delgado	
 * 					
 * 
 * The TestTree class allows the user to open an input file using Java's
 * graphical file chooser. It expects a file with the first line containing
 * attribute names, separated only by spaces. Then it expects the following 
 * lines to contain the records and their values for each attribute. 
 * 
 * If the input is parsed correctly, the program goes on to build a
 * decision tree, using information gain as the attribute selection 
 * method. After that, a graphical representation of the tree is 
 * printed to a file called tree.txt in the current directory and
 * it is displayed in a scrollable text box. 
 * 
 *  Finally, the user is prompted to enter a single record to be
 *  classified. A classification  is made and the result printed 
 *  to JOptionPane dialog box. 
 */


import java.awt.Dimension;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import javax.swing.JOptionPane;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;


public class TestTree {

	public static void main(String[] args) {

		DecisionTree tree = new DecisionTree();
		boolean status = tree.parseInput();
		if(status)
		{
			try
			{

				tree.buildTree(tree.root);
				tree.graphTree(tree.root, "\t" );
				tree.out.close();

				//Displaying Output File in a JTextArea
				BufferedReader br = new BufferedReader(new FileReader("tree.txt"));
				JTextArea textArea = new JTextArea();
				textArea.read(br, true);
				JScrollPane scrollPane = new JScrollPane(textArea);
				textArea.setWrapStyleWord(true);
				scrollPane.setPreferredSize(new Dimension(900, 650));
				JOptionPane.showMessageDialog(null, scrollPane, "tree.txt", JOptionPane.INFORMATION_MESSAGE);
				br.close();

				tree.readAndClassifyTuple();

			}
			catch (NumberFormatException | NullPointerException | IOException e) 
			{
				System.err.println(e.toString());
			}


		}

	}

}
