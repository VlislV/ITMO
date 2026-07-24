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

    // ==================== ТЕСТЫ ВАЛИДАЦИИ ====================

    @Test
    public void testValidXValues() throws Exception {
        point.setX(2); point.setY(0.0); point.setR(3.0);
        String result = checker.check(point);
        assertNotNull(result);
    }

    @Test(expected = Exception.class)
    public void testInvalidXTooLarge() throws Exception {
        point.setX(3); point.setY(0.0); point.setR(3.0);
        checker.check(point);
    }

    @Test(expected = Exception.class)
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

    @Test(expected = Exception.class)
    public void testYBelowLowerBound() throws Exception {
        point.setX(0); point.setY(-3.1); point.setR(3.0);
        checker.check(point);
    }

    @Test(expected = Exception.class)
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

    @Test(expected = Exception.class)
    public void testRBelowLowerBound() throws Exception {
        point.setX(0); point.setY(0.0); point.setR(1.9);
        checker.check(point);
    }

    @Test(expected = Exception.class)
    public void testRAboveUpperBound() throws Exception {
        point.setX(0); point.setY(0.0); point.setR(5.1);
        checker.check(point);
    }

    // ==================== ТЕСТЫ ПОПАДАНИЯ: ТРЕУГОЛЬНИК ====================

    @Test
    public void testHitTriangleInside() throws Exception {
        // Точка внутри треугольника: X=-1, Y=1, R=4
        // 2*1 = 2 <= -1 + 4 = 3 ✓, Y=1 >= 0 ✓, X=-1 <= 0 ✓
        point.setX(-1); point.setY(1.0); point.setR(4.0);
        assertTrue(checker.check(point).contains("triangle"));
    }

    @Test
    public void testHitTriangleBoundary() throws Exception {
        // Точка на границе: 2Y = X + R -> Y = (X+R)/2
        // Для X=-1, R=4: Y = (-1+4)/2 = 1.5
        point.setX(-1); point.setY(1.5); point.setR(4.0);
        assertTrue(checker.check(point).contains("triangle"));
    }

    @Test
    public void testHitTriangleOrigin() throws Exception {
        // Вершина треугольника в (0,0): 2*0 = 0 <= 0+4
        point.setX(0); point.setY(0.0); point.setR(4.0);
        assertTrue(checker.check(point).contains("triangle"));
    }

    @Test
    public void testMissTriangleOutside() throws Exception {
        // Точка выше треугольника: 2*3 = 6 > -1+4 = 3
        point.setX(-1); point.setY(3.0); point.setR(4.0);
        assertFalse(checker.check(point).contains("triangle"));
    }

    // ==================== ТЕСТЫ ПОПАДАНИЯ: ПРЯМОУГОЛЬНИК ====================

    @Test
    public void testHitRectangleInside() throws Exception {
        // X=1, Y=1, R=4: X<R (1<4) ✓, Y<R/2 (1<2) ✓
        point.setX(1); point.setY(1.0); point.setR(4.0);
        assertTrue(checker.check(point).contains("rectangle"));
    }

    @Test
    public void testHitRectangleCorner() throws Exception {
        // Угол прямоугольника: X=3.9, Y=1.9, R=4
        point.setX(1); point.setY(1.9); point.setR(4.0);
        assertTrue(checker.check(point).contains("rectangle"));
    }

    @Test
    public void testMissRectangleXTooLarge() throws Exception {
        // X=4 при R=4: X<R (4<4) = false
        point.setX(4); point.setY(1.0); point.setR(4.0);
        assertFalse(checker.check(point).contains("rectangle"));
    }

    @Test
    public void testMissRectangleYTooLarge() throws Exception {
        // Y=2 при R=4: Y<R/2 (2<2) = false
        point.setX(1); point.setY(2.0); point.setR(4.0);
        assertFalse(checker.check(point).contains("rectangle"));
    }

    // ==================== ТЕСТЫ ПОПАДАНИЯ: КРУГ ====================

    @Test
    public void testHitCircleInside() throws Exception {
        // X=-2, Y=-2, R=4: 4+4=8 <= 16 ✓
        point.setX(-2); point.setY(-2.0); point.setR(4.0);
        assertTrue(checker.check(point).contains("circle"));
    }

    @Test
    public void testHitCircleBoundary() throws Exception {
        // X=-4, Y=0, R=4: 16+0=16 <= 16 ✓
        point.setX(-4); point.setY(0.0); point.setR(4.0);
        assertTrue(checker.check(point).contains("circle"));
    }

    @Test
    public void testHitCircleCorner() throws Exception {
        // X=-2√2 ≈ -2.828, Y=-2√2 ≈ -2.828, R=4: 8+8=16 <= 16 ✓
        point.setX(-2); point.setY(-3.0); point.setR(4.0);
        // 4+9=13 <= 16 ✓
        assertTrue(checker.check(point).contains("circle"));
    }

    @Test
    public void testMissCircleOutside() throws Exception {
        // X=-3, Y=-3, R=4: 9+9=18 > 16
        point.setX(-3); point.setY(-3.0); point.setR(4.0);
        assertFalse(checker.check(point).contains("circle"));
    }

    // ==================== ТЕСТЫ ПРОМАХА ====================

    @Test
    public void testMissFarOutside() throws Exception {
        // Точка далеко от всех областей
        point.setX(3); point.setY(4.0); point.setR(3.0);
        assertEquals("MISS", checker.check(point));
    }

    @Test
    public void testMissInFourthQuadrant() throws Exception {
        // Четвёртый квадрант (X>0, Y<0) — нет областей
        point.setX(1); point.setY(-1.0); point.setR(3.0);
        assertEquals("MISS", checker.check(point));
    }

    // ==================== ГРАНИЧНЫЕ ТЕСТЫ ====================

    @Test
    public void testEdgeCaseMinRMaxX() throws Exception {
        // Минимальный R, максимальный валидный X
        point.setX(2); point.setY(0.0); point.setR(2.0);
        String result = checker.check(point);
        assertNotNull(result);
    }

    @Test
    public void testEdgeCaseMaxRMinX() throws Exception {
        // Максимальный R, минимальный валидный X
        point.setX(-2); point.setY(5.0); point.setR(5.0);
        String result = checker.check(point);
        assertNotNull(result);
    }

    // ==================== ТЕСТ РЕЗУЛЬТАТА СТРОКИ ====================

    @Test
    public void testResultIsHitOrMiss() throws Exception {
        for (int x : new int[]{-2, -1, 0, 1, 2}) {
            for (double y : new double[]{-3.0, 0.0, 3.0, 5.0}) {
                for (double r : new double[]{2.0, 3.5, 5.0}) {
                    point.setX(x); point.setY(y); point.setR(r);
                    String result = checker.check(point);
                    // Результат должен быть либо HIT, либо MISS
                    assertTrue(
                            "Неожиданный результат: " + result,
                            result.startsWith("HIT") || result.equals("MISS")
                    );
                }
            }
        }
    }
}