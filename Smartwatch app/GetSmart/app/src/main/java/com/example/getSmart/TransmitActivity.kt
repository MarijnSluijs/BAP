package com.example.getSmart

import android.app.Activity
import android.content.Intent
import android.hardware.Sensor
import android.hardware.SensorEvent
import android.hardware.SensorEventListener
import android.hardware.SensorManager
import android.os.Bundle
import android.view.WindowManager
import android.widget.Button
import android.widget.TextView
import com.example.getSmart.databinding.ActivityTransmitBinding
import java.io.File
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter
import kotlin.concurrent.fixedRateTimer

class TransmitActivity : Activity() , SensorEventListener{

    private lateinit var binding: ActivityTransmitBinding

    //Initialize sensors
    private lateinit var sensorManager: SensorManager
    private var light: Sensor? = null
    private var accel: Sensor? = null
    private var grav: Sensor? = null
    private var gyro: Sensor? = null
    private var linac: Sensor? = null
    private var rotat: Sensor? = null
    private var hrate: Sensor? = null
    private var xaccel: Float = 0F
    private var yaccel: Float = 0F
    private var zaccel: Float = 0F
    private var xgyro: Float = 0F
    private var ygyro: Float = 0F
    private var zgyro: Float = 0F
    private var hvalue = "0"
    private val transmit = TransmissionService()
    private var stop: Boolean = false

    //Set samplingPeriod and send interval
    private val samplingPeriod: Long = 20    //Sensor sampling period in ms
    private val sendInterval: Int = 10000      //Interval between batch of samples send to the server in miliseconds

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding = ActivityTransmitBinding.inflate(layoutInflater)
        setContentView(binding.root)

        //Setup sensors
        sensorSetup()

        //Keep the screen on when transmitting data
        window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)

        // token is the time at the start of the recording, using this it is possible to distinguish recording sessions
        val token = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd:HH:mm:ss.SSS"))

        //Read the userID from the internal storage
        val userID = File(getDir("userID", 0), "userID.txt").readText()

        //Find current activity
        val activity = intent.getStringExtra("activity").toString()

        val text: TextView = findViewById(R.id.text)
        text.text = "Smartwatch is now recording."

        val dataSet = mutableListOf<Data>()
        var i=0
        var j = 0
        //Acquire sensor data every samplingPeriod and transmit data every transmitPeriod
        fixedRateTimer("timer", true, 100, samplingPeriod) {
            //Timer continues until stop recording button is clicked
            if (!stop) {
                val data = Data(
                    user = userID,
                    acceX = xaccel,
                    acceY = yaccel,
                    acceZ = zaccel,
                    gyroX = xgyro,
                    gyroY = ygyro,
                    gyroZ = zgyro,
                    bpm = hvalue,
                    token = token,
                    label = activity
                )
                //dataSet is empty at first, dataSet.add adds new object to the list.
                //The next sendInterval the data needs to be overwritten, so dataSet[i] = data is used.
                if(j == 0){
                    dataSet.add(data)
                } else {
                    dataSet[i] = data
                }

                //Transmit the data every sendInterval
                if (i == (((sendInterval)/samplingPeriod)-1).toInt()){
                    //Padding the array to 50 samples for testing the battery life
//                    if(j == 0) {
//                        while (i < 49) {
//                            dataSet.add(data)
//                            i++
//                        }
//                    }

                    transmit.transmitData(dataSet)
                    i=0
                    j=1
                }else{
                    i++
                }
            } else {
                this.cancel()
            }
        }

        //Go back to the main activity when stop button is clicked
        val stopButton: Button = findViewById(R.id.stopButton)
        stopButton.setOnClickListener{
            stop = true
            stopButton.context.startActivity(Intent(stopButton.context, MainActivity::class.java))
        }
    }

    //Sensor setup
    private fun sensorSetup(){
        sensorManager = getSystemService(SENSOR_SERVICE) as SensorManager

        accel = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER)
        light = sensorManager.getDefaultSensor(Sensor.TYPE_LIGHT)
        grav = sensorManager.getDefaultSensor(Sensor.TYPE_GRAVITY)
        gyro = sensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE)
        linac = sensorManager.getDefaultSensor(Sensor.TYPE_LINEAR_ACCELERATION)
        rotat = sensorManager.getDefaultSensor(Sensor.TYPE_ROTATION_VECTOR)
        hrate = sensorManager.getDefaultSensor(Sensor.TYPE_HEART_RATE)

        accel?.also { accelerometer ->
            sensorManager.registerListener(this, accelerometer, (samplingPeriod*1000).toInt())
        }
        gyro?.also { light ->
            sensorManager.registerListener(this, light, (samplingPeriod*1000).toInt())
        }
        hrate?.also { light ->
            sensorManager.registerListener(this, light, (samplingPeriod*1000).toInt())
        }
    }

    // Receive sensor data
    override fun onSensorChanged(event: SensorEvent) {

        // Accelerometer
        if((event.sensor.type == Sensor.TYPE_ACCELEROMETER)) {
            xaccel = event.values[0].toString().toFloat()
            yaccel = event.values[1].toString().toFloat()
            zaccel = event.values[2].toString().toFloat()
        }

        // Gyroscope
        if(event.sensor.type == Sensor.TYPE_GYROSCOPE) {
            xgyro = event.values[0].toString().toFloat()
            ygyro = event.values[1].toString().toFloat()
            zgyro = event.values[2].toString().toFloat()
        }

        // Heartrate
        if(event.sensor.type == Sensor.TYPE_HEART_RATE) {
            hvalue = event.values[0].toString()
        }
    }

    // Detect accuracy change of sensor
    override fun onAccuracyChanged(sensor: Sensor, accuracy: Int) {
    }

    override fun onBackPressed() {}
}