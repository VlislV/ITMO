package Utils;

import org.junit.*;
import java.sql.*;
import static org.junit.Assert.*;

public class DbManagerTest {
    private Connection conn;

    @BeforeClass
    public static void setUpClass() {
        DbManager.loadProperties("test-database.properties");
    }

    @Before
    public void setUp() throws SQLException {
        conn = DbManager.getConnection();
    }

    @After
    public void tearDown() throws SQLException {
        if (conn != null) {
            Statement stmt = conn.createStatement();
            stmt.execute("DROP TABLE points");
            stmt.close();
            conn.close();
        }
    }

    @Test
    public void testConnectionIsNotNull() {
        assertNotNull(conn);
    }

    @Test
    public void testTableExists() throws SQLException {
        Statement stmt = conn.createStatement();
        stmt.execute("SELECT * FROM points");  // если таблицы нет — упадёт
        stmt.close();
    }

    @Test
    public void testInsertAndCount() throws SQLException {
        Statement stmt = conn.createStatement();

        stmt.execute("INSERT INTO points (x, y, r, result) VALUES (1, 2.0, 3.0, 'hit')");
        stmt.execute("INSERT INTO points (x, y, r, result) VALUES (-1, -2.0, 3.0, 'miss')");

        ResultSet rs = stmt.executeQuery("SELECT COUNT(*) FROM points");
        rs.next();
        assertEquals(2, rs.getInt(1));

        rs.close();
        stmt.close();
    }
}
