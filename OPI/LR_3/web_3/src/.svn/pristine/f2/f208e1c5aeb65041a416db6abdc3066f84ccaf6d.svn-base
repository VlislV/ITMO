package Utils;

import beans.PointBean;
import jakarta.xml.bind.ValidationException;
import java.util.ResourceBundle;
import java.util.Arrays;
import java.util.concurrent.atomic.AtomicReference;

public class Checker {
    private AtomicReference<Integer> X = new AtomicReference<Integer>();
    private AtomicReference<Double> Y = new AtomicReference<Double>();
    private AtomicReference<Double> R = new AtomicReference<Double>();
    private final Integer[] validX = {-2, -1, 0, 1, 2};

    private static final ResourceBundle messages =
            ResourceBundle.getBundle("locales.messages");

    private void validate() throws ValidationException {
        if (!Arrays.asList(validX).contains(X.get())) {
            throw new ValidationException(
                    messages.getString("validation.error.x")
            );
        }
        if (Y.get() < -3 || Y.get() > 5) {
            throw new ValidationException(
                    messages.getString("validation.error.y")
            );
        }
        if (R.get() < 2 || R.get() > 5) {
            throw new ValidationException(
                    messages.getString("validation.error.r")
            );
        }
    }

    public String check(PointBean point) throws Exception {
        X.set(Integer.parseInt(point.getX().toString()));
        Y.set(Double.parseDouble(point.getY().toString()));
        R.set(Double.parseDouble(point.getR().toString()));
        validate();

        if (Y.get() >= 0 && X.get() <= 0 && 2 * Y.get() <= X.get() + R.get())
            return messages.getString("result.hit.triangle");
        if (Y.get() >= 0 && X.get() >= 0 && X.get() < R.get() && Y.get() < R.get() / 2)
            return messages.getString("result.hit.rectangle");
        if (X.get() <= 0 && Y.get() <= 0 && X.get() * X.get() + Y.get() * Y.get() <= (double) R.get() * R.get())
            return messages.getString("result.hit.circle");
        return messages.getString("result.miss");
    }
}