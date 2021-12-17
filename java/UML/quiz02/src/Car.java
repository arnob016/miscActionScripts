
/**
 *
 * @author alpha4d
 */


interface Drive{
    public void start();
    public void stop();
}

class Vehicle {
    
    
    public String model;

    public Vehicle(String model) {
        this.model = model;
    }
    
    public void display(){
        System.out.println("Mode: "+ model);
    }
    
    
}

class Car extends Vehicle implements Drive{
    
    private double price;
    
    public Car(String model, double price){
        super(model);
        this.price = price;
    }
    
    @Override
    public void display(){
         super.display();
         System.out.println("Price: "+price);
     }
    
    @Override
    public void start(){
        System.out.println(model+" is starting..");
    }
    
    @Override
    public void stop(){
        System.out.println(model+" is stoping..");
    }
    
    public static void main(String[] args){
        Car car = new Car("S3", 20000.32);
        
        car.display();
        car.start();
        car.stop();
    }
}

