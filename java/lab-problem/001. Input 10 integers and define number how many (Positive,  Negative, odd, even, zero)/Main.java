import java.util.Scanner;
public class Main {

    public static void main(String[] args) {
        int[] dN = {0, 0, 0, 0, 0}; //0 p, 1 n, 2 o, 3 e, 4 z;
        int[] fromUserIn = new int[10];
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter 10 number: ");
        for (int x = 0; x < 10; x++) {
            fromUserIn[x] = sc.nextInt();
        }
        for (int a : fromUserIn) {
            dN[0] = a > 0 ? ++dN[0] : dN[0];
            dN[1] = a < 0 ? ++dN[1] : dN[1];
            if (a % 2 == 0) {
                dN[3]++;
            } else {
                dN[2]++;
            }
            dN[4] = a == 0 ? ++dN[4] : dN[4];
        }
        String output = String.format(
                "%d Number of positive numbers.\n"
                + "%d Number of negative numbers.\n"
                + "%d Number of odd numbers.\n"
                + "%d Number of even numbers.\n"
                + "%d Number of zero numbers.",
                 dN[0], dN[1], dN[2], dN[3], dN[4]);
        System.out.println(output);
    }
}
