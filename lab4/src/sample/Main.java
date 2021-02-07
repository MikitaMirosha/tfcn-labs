package sample;

import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;
import javafx.scene.input.KeyCode;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

import java.util.Random;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class Main extends Application {

    private static TextField inputTextField;
    private static TextField outputTextField;
    private static TextArea statusTextArea;

    public static void main(String[] args) {
        launch(args);
    }

    public static class ChildRunnable implements Runnable {

        private final String string;
        private final int maxValue;

        public ChildRunnable(String string, int maxValue) {
            this.string = string;
            this.maxValue = maxValue;
        }

        @Override
        public void run() {
            for (String letter : string.split("")) {
                boolean collision;
                boolean busyChannel;

                for (int i = 0; i < maxValue; ) {
                    while(true) {
                        try {
                            busyChannel = ((int)(Math.random() * 10) <= 3);
                            if(busyChannel)
                                Thread.sleep(100);
                            else break;
                        } catch (InterruptedException ex) {
                            ex.printStackTrace();
                        }
                    }
                    try {
                        //outputTextField.appendText(letter);
                        Thread.sleep(500);
                    } catch (InterruptedException ex) {
                        ex.printStackTrace();
                    }
                    collision = ((int)(Math.random() * 10) <= 3);
                    if (collision) {
                        statusTextArea.appendText("*");
                        i++;
                        if (i == maxValue) break;
                        try {
                            Thread.sleep(new Random().nextInt((int) Math.pow(2, i)));
                        } catch (InterruptedException ex) {
                            ex.printStackTrace();
                        }
                    } else {
                        if (i == 0) statusTextArea.appendText("");
                        outputTextField.appendText(letter);
                        break;
                    }
                }
                statusTextArea.appendText("\n");
            }
        }
    }

    @Override
    public void start(Stage stage) {

        graphics(stage);

        inputTextField.setOnKeyReleased(e -> {
            if (e.getCode().equals(KeyCode.ENTER)) {
                outputTextField.clear();
                statusTextArea.clear();
                String inputText = inputTextField.getText();
                if(!inputText.isEmpty()) {
                    int maxValue = 5;
                    ExecutorService executor = Executors.newSingleThreadExecutor();
                    executor.execute(new ChildRunnable(inputText, maxValue));
                }
            }
        });
    }

    public static void graphics(Stage stage) {

        stage.setTitle("CSMA");
        stage.setWidth(400);
        stage.setHeight(400);
        stage.setResizable(false);

        Label inputLabel = new Label("INPUT");
        inputTextField = new TextField();

        Label outputLabel = new Label("OUTPUT");
        outputTextField = new TextField();
        outputTextField.setEditable(false);

        Label statusLabel = new Label("STATUS");
        statusTextArea = new TextArea();
        statusTextArea.setEditable(false);
        statusTextArea.setPrefHeight(300);

        VBox vBox = new VBox(7, inputLabel, inputTextField, outputLabel,
                outputTextField, statusLabel, statusTextArea);
        vBox.setPadding(new Insets(7));
        vBox.setAlignment(Pos.CENTER);

        stage.setScene(new Scene(vBox));
        stage.show();
    }
}
