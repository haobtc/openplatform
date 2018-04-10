package demo;

import java.security.Key;
import java.security.NoSuchAlgorithmException;
import java.security.NoSuchProviderException;
import java.security.SecureRandom;
import java.security.Security;

import javax.crypto.Cipher;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;

import org.bouncycastle.jce.provider.BouncyCastleProvider;
import org.bouncycastle.util.Arrays;

import sun.misc.BASE64Decoder;
import sun.misc.BASE64Encoder;

@SuppressWarnings({ "unused", "restriction" })
public class AES {

  private static final int blockSize = 16;
  static  final String KEY_ALGORITHM = "AES";
  // 加解密算法/模式/填充方式
  static  final String algorithmStr = "AES/CBC/PKCS7Padding";
  private static Key key;
  private static Cipher cipher;
  private static byte[] iv = new byte[blockSize];

  public static void init(String aesKey) {

    byte[] keyBytes = aesKey.getBytes();
    // 初始化
    Security.addProvider(new BouncyCastleProvider());
    // 转化成JAVA的密钥格式
    key = new SecretKeySpec(keyBytes, KEY_ALGORITHM);
    try {
        // 初始化cipher
        cipher = Cipher.getInstance(algorithmStr, "BC");
    } catch (NoSuchAlgorithmException e) {
        // TODO Auto-generated catch block
        e.printStackTrace();
    } catch (NoSuchPaddingException e) {
        // TODO Auto-generated catch block
        e.printStackTrace();
    } catch (NoSuchProviderException e) {
        // TODO Auto-generated catch block
        e.printStackTrace();
    }
  }

  // 加密
  public static String Encrypt(String vendorKey, String data) throws Exception {

    init(vendorKey);

    SecureRandom randomSecureRandom = SecureRandom.getInstance("SHA1PRNG");
    randomSecureRandom.nextBytes(iv);
    IvParameterSpec ivParams = new IvParameterSpec(iv);
    cipher.init(Cipher.ENCRYPT_MODE, key, ivParams);

    String content = addPadding(data);
    byte[] encrypted = cipher.doFinal(content.getBytes());
    return base64Encode(concat(iv, encrypted));
  }

  public static byte[] concat(byte[] b1, byte[] b2) {
    byte[] b3 = new byte[b1.length + b2.length];
    System.arraycopy(b1, 0, b3, 0, b1.length);
    System.arraycopy(b2, 0, b3, b1.length, b2.length);
    return b3;
  }

  public static String addPadding(String content) {
     int paddingLength = blockSize - content.length() % blockSize;
     for(int i=0; i<paddingLength; i++) {
       content += (char)paddingLength;
     }
     return content;
  }

  public static String deletePadding(String content) {
    int paddingLength = (int)(content.charAt(content.length() - 1));
    return content.substring(0, content.length() - paddingLength);
  }

  public static String base64Encode(byte[] bytes){
    return new BASE64Encoder().encode(bytes);
  }

  public static byte[] base64Decode(String base64Code) throws Exception{
    return new BASE64Decoder().decodeBuffer(base64Code);
  }

  // 解密
  public static String Decrypt(String vendorKey, String content) throws Exception {

    byte[] data = base64Decode(content);
    byte[] iv = new byte[blockSize];
    byte[] raw = new byte[data.length - blockSize];
    System.arraycopy(data, 0, iv, 0, blockSize);
    System.arraycopy(data, blockSize, raw, 0, data.length - blockSize);

    init(vendorKey);

    IvParameterSpec ivParam = new IvParameterSpec(iv);
    cipher.init(Cipher.DECRYPT_MODE, key, ivParam);

    byte[] original = cipher.doFinal(raw);
    String originalString = new String(original);
    return deletePadding(originalString);
  }

  public static void main(String[] args) throws Exception {
    String vendorKey = "ed2f48dee4e14d6391044a11bdb2cee3";
    // 需要加密的字串
    String text = "{'event_id': 'event-id', 'vendor_name': 'your-vendor-name', 'payload': {'note': '', 'user.id': 123, 'amount': 100, 'transfer.id': 12, 'json_args': {'arg1': '111111'}}, 'subject': 'user2vendor.created'}";
    // 加密
    String encryptStirng = AES.Encrypt(vendorKey, text);
    System.out.println("加密后的字串是：" + encryptStirng);

    // 解密
    String DecryptString = AES.Decrypt(vendorKey, encryptStirng);
    System.out.println("解密后的字串是：" + DecryptString);
  }
}
