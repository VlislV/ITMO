class C {
  int p32;
  int p16;
  int p31;
  int p30;
  int p13;
  long p9;
  long p23;
  long p8;
  int[] p19 = {-3, 0, 0, 3, 3};
  int[] p2 = {2, 3, -1, -1, 3};
  int[] p11 = {-1, -1, -1, 3, -2};
  static int p7;
  static int p39;
  static int p38;
  static int p35;
  static int p36;
  public C() {
    p32 = 6;
    p16 = 2;
    p31 = 3;
    p30 = 3;
    p13 = 9;
    p9 = 2L;
    p23 = 9L;
    p8 = 9L;
  }
  public void p34() {
    System.out.println("метод p34 в классе C");
    System.out.println(p30);
  }
  public void p20() {
    System.out.println("метод p20 в классе C");
    System.out.println(p30 >> 2);
  }
  public void p26() {
    System.out.println("метод p26 в классе C");
    System.out.println(p32 << 2);
  }
  public void p28() {
    System.out.println("метод p28 в классе C");
    System.out.println(p13);
  }
  public void p25() {
    System.out.println("метод p25 в классе C");
    System.out.println((int)p8);
  }
  public void p14() {
    System.out.println("метод p14 в классе C");
    System.out.println(p39++);
  }
  public static void p1() {
    System.out.println("метод p1 в классе C");
    System.out.println(p35);
  }
  public static void p37() {
    System.out.println("метод p37 в классе C");
    System.out.println((p35 - 5));
  }
  public static void p18() {
    System.out.println("метод p18 в классе C");
    System.out.println(p36);
  }
  public static void p24() {
    System.out.println("метод p24 в классе C");
    System.out.println((p36 - 3));
  }
  public void p10(C r) {
    r.p34();
  }
  public void p10(E r) {
    r.p20();
  }
}
