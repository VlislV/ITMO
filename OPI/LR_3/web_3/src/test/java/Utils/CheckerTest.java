package Utils;

import beans.PointBean;
import jakarta.xml.bind.ValidationException;
import org.junit.*;
import static org.junit.Assert.*;

public class CheckerTest {

    private Checker checker;
    private PointBean point;

    @Before
    public void setUp() {
        checker = new Checker();
        point = new PointBean();
    }

    @Test
    public void testValidXValues() throws Exception {
        point.setX(2); point.setY(0.0); point.setR(3.0);
        String result = checker.check(point);
        assertNotNull(result);
    }

    @Test(expected = ValidationException.class)
    public void testInvalidXTooLarge() throws Exception {
        point.setX(3); point.setY(0.0); point.setR(3.0);
        checker.check(point);
    }

    @Test(expected = ValidationException.class)
    public void testInvalidXTooSmall() throws Exception {
        point.setX(-3); point.setY(0.0); point.setR(3.0);
        checker.check(point);
    }

    @Test
    public void testAllValidXValues() throws Exception {
        for (int x : new int[]{-2, -1, 0, 1, 2}) {
            point.setX(x);
            point.setY(0.0);
            point.setR(3.0);
            String result = checker.check(point);
            assertNotNull("Должен пройти для X=" + x, result);
        }
    }

    @Test
    public void testYLowerBound() throws Exception {
        point.setX(0); point.setY(-3.0); point.setR(3.0);
        String result = checker.check(point);
        assertNotNull("Y=-3 должно быть валидным", result);
    }

    @Test
    public void testYUpperBound() throws Exception {
        point.setX(0); point.setY(5.0); point.setR(3.0);
        String result = checker.check(point);
        assertNotNull("Y=5 должно быть валидным", result);
    }

    @Test(expected = ValidationException.class)
    public void testYBelowLowerBound() throws Exception {
        point.setX(0); point.setY(-3.1); point.setR(3.0);
        checker.check(point);
    }

    @Test(expected = ValidationException.class)
    public void testYAboveUpperBound() throws Exception {
        point.setX(0); point.setY(5.1); point.setR(3.0);
        checker.check(point);
    }

    @Test
    public void testRLowerBound() throws Exception {
        point.setX(0); point.setY(0.0); point.setR(2.0);
        String result = checker.check(point);
        assertNotNull("R=2 должно быть валидным", result);
    }

    @Test
    public void testRUpperBound() throws Exception {
        point.setX(0); point.setY(0.0); point.setR(5.0);
        String result = checker.check(point);
        assertNotNull("R=5 должно быть валидным", result);
    }

    @Test(expected = ValidationException.class)
    public void testRBelowLowerBound() throws Exception {
        point.setX(0); point.setY(0.0); point.setR(1.9);
        checker.check(point);
    }

    @Test(expected = ValidationException.class)
    public void testRAboveUpperBound() throws Exception {
        point.setX(0); point.setY(0.0); point.setR(5.1);
        checker.check(point);
    }

    private boolean resultContains(String result, String... keywords) {
        for (String keyword : keywords) {
            if (result != null && result.contains(keyword)) {
                return true;
            }
        }
        return false;
    }

    private boolean isMiss(String result) {
        return result != null && (result.equals("MISS") || result.equals("Промах"));
    }

    @Test
    public void testHitTriangleInside() throws Exception {
        point.setX(-1); point.setY(1.0); point.setR(4.0);
        String result = checker.check(point);
        assertTrue("Ожидалось попадание в треугольник, но получено: " + result,
                resultContains(result, "triangle", "треугольник"));
    }

    @Test
    public void testHitTriangleBoundary() throws Exception {
        point.setX(-1); point.setY(1.5); point.setR(4.0);
        String result = checker.check(point);
        assertTrue("Ожидалось попадание в треугольник, но получено: " + result,
                resultContains(result, "triangle", "треугольник"));
    }

    @Test
    public void testHitTriangleOrigin() throws Exception {
        point.setX(0); point.setY(0.0); point.setR(4.0);
        String result = checker.check(point);
        assertTrue("Ожидалось попадание в треугольник, но получено: " + result,
                resultContains(result, "triangle", "треугольник"));
    }

    @Test
    public void testMissTriangleOutside() throws Exception {
        point.setX(-1); point.setY(3.0); point.setR(4.0);
        String result = checker.check(point);
        assertFalse("Не ожидалось попадание в треугольник, но получено: " + result,
                resultContains(result, "triangle", "треугольник"));
    }

    @Test
    public void testHitRectangleInside() throws Exception {
        point.setX(1); point.setY(1.0); point.setR(4.0);
        String result = checker.check(point);
        assertTrue("Ожидалось попадание в прямоугольник, но получено: " + result,
                resultContains(result, "rectangle", "прямоугольник"));
    }

    @Test
    public void testHitRectangleCorner() throws Exception {
        point.setX(1); point.setY(1.9); point.setR(4.0);
        String result = checker.check(point);
        assertTrue("Ожидалось попадание в прямоугольник, но получено: " + result,
                resultContains(result, "rectangle", "прямоугольник"));
    }

    @Test
    public void testMissRectangleXTooLarge() throws Exception {
        point.setX(2); point.setY(1.0); point.setR(2.0);
        String result = checker.check(point);
        assertFalse("Не ожидалось попадание в прямоугольник, но получено: " + result,
                resultContains(result, "rectangle", "прямоугольник"));
    }

    @Test
    public void testMissRectangleYTooLarge() throws Exception {
        point.setX(1); point.setY(2.0); point.setR(4.0);
        String result = checker.check(point);
        assertFalse("Не ожидалось попадание в прямоугольник, но получено: " + result,
                resultContains(result, "rectangle", "прямоугольник"));
    }

    @Test
    public void testHitCircleInside() throws Exception {
        point.setX(-2); point.setY(-2.0); point.setR(4.0);
        String result = checker.check(point);
        assertTrue("Ожидалось попадание в круг, но получено: " + result,
                resultContains(result, "circle", "круг"));
    }

    @Test
    public void testHitCircleBoundary() throws Exception {
        point.setX(-2); point.setY(-2.0); point.setR(3.0);
        String result = checker.check(point);
        assertTrue("Ожидалось попадание в круг, но получено: " + result,
                resultContains(result, "circle", "круг"));
    }

    @Test
    public void testHitCircleCorner() throws Exception {
        point.setX(-2); point.setY(-2.0); point.setR(4.0);
        String result = checker.check(point);
        assertTrue("Ожидалось попадание в круг, но получено: " + result,
                resultContains(result, "circle", "круг"));
    }

    @Test
    public void testMissCircleOutside() throws Exception {
        point.setX(-2); point.setY(-3.0); point.setR(2.0);
        String result = checker.check(point);
        assertFalse("Не ожидалось попадание в круг, но получено: " + result,
                resultContains(result, "circle", "круг"));
    }

    @Test
    public void testMissFarOutside() throws Exception {
        point.setX(2); point.setY(4.0); point.setR(3.0);
        String result = checker.check(point);
        assertTrue("Ожидался промах, но получено: " + result, isMiss(result));
    }

    @Test
    public void testMissInFourthQuadrant() throws Exception {
        point.setX(1); point.setY(-1.0); point.setR(3.0);
        String result = checker.check(point);
        assertTrue("Ожидался промах, но получено: " + result, isMiss(result));
    }

    @Test
    public void testEdgeCaseMinRMaxX() throws Exception {
        point.setX(2); point.setY(0.0); point.setR(2.0);
        String result = checker.check(point);
        assertNotNull(result);
    }

    @Test
    public void testEdgeCaseMaxRMinX() throws Exception {
        point.setX(-2); point.setY(5.0); point.setR(5.0);
        String result = checker.check(point);
        assertNotNull(result);
    }

    @Test
    public void testResultIsHitOrMiss() throws Exception {
        for (int x : new int[]{-2, -1, 0, 1, 2}) {
            for (double y : new double[]{-3.0, 0.0, 3.0, 5.0}) {
                for (double r : new double[]{2.0, 3.0, 4.0, 5.0}) {
                    point.setX(x); point.setY(y); point.setR(r);
                    String result = checker.check(point);
                    boolean isValid = isMiss(result) ||
                            resultContains(result, "HIT", "попадание") ||
                            resultContains(result, "circle", "круг") ||
                            resultContains(result, "rectangle", "прямоугольник") ||
                            resultContains(result, "triangle", "треугольник");
                    assertTrue(
                            "Неожиданный результат: " + result + " для x=" + x + ", y=" + y + ", r=" + r,
                            isValid
                    );
                }
            }
        }
    }
}