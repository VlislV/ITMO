package beans;

public interface HitMBean {
    int getTotalPoints();
    int getHits();
    void checkPointOutOfBounds(int x, double y, double r);
}