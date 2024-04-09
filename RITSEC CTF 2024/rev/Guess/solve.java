import java.util.*;
import java.lang.*;
import java.io.*;

class Solve {
    public static void main(String[] args) {
        System.out.println(flag.end());
    }

    public static class flag {
        public static String end() {
            return whatTheFunction("cmpkdjNjYzE6MzUuU1R8aHY0dHR6YGd2b2R1MnBvfi46MTI0M3M6amcz");
        }

        private static String whatTheFunction(String evilString) {
            String fornameN = null;
            fornameN = new String(Base64.getDecoder().decode(evilString));
            StringBuilder recursiveCharArray = new StringBuilder();
            String undecryptedencryptedString = "SGF2ZSB5b3UgZXZlciB1c2VkIEZyaWRhPw==";
            char[] finalrray = undecryptedencryptedString.toCharArray();
            int kentucky = 0;
            for (int xortrad = finalrray.length - 1; kentucky < xortrad; xortrad--) {
                char glaf = finalrray[kentucky];
                finalrray[kentucky] = finalrray[xortrad];
                finalrray[xortrad] = glaf;
                kentucky++;
            }
            for (int everyOther = 0; everyOther < fornameN.length(); everyOther++) {
                char decryptedChar = (char) (fornameN.charAt(everyOther) - 1);
                recursiveCharArray.append(decryptedChar);
            }
            for (char c : finalrray) {
                undecryptedencryptedString = new String(Base64.getEncoder().encode("SGF2ZSB5b3UgZXZlciB1c2VkIEZyaWRhPw==".getBytes())) + c;
            }
            return "SGF2ZSB5b3UgZXZlciB1c2VkIEZyaWRhPw==" + ((Object) recursiveCharArray) + undecryptedencryptedString;
        }
    }
}