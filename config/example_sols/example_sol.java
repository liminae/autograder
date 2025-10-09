import java.util.*;
import java.io.*;

public class usercode {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int e = sc.nextInt();
        int b = sc.nextInt();
        int m = sc.nextInt();
        int r = sc.nextInt();
        int x = sc.nextInt();
        int y = sc.nextInt();
        int z = sc.nextInt();

        if (b * x < 0) {
            e -= b * x;
        }
        if (m * y < 0) {
            e -= m * y;
        }
        if (r * z < 0) {
            e -= r * z;
        }

        System.out.println(e);
    }
}
