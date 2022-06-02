package com.example.datatransmission

import android.Manifest
import android.app.Activity
import android.content.ContentValues
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
import android.util.Log
import android.view.View
import android.widget.*
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import com.example.datatransmission.R.id.ChangeIdButton
import com.example.datatransmission.databinding.ActivityMainBinding
import com.google.android.gms.wearable.Wearable
import java.io.File
import java.util.*

class MainActivity : Activity() {

    private lateinit var binding: ActivityMainBinding

    private val reqcode = 101

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        //Assign UI elements to values
        val recordText : TextView = findViewById(R.id.recordText)
        val recordButton : TextView = findViewById(R.id.recordButton)
        val changeId : Button = findViewById(ChangeIdButton)
        val idText : TextView = findViewById(R.id.idText)
        val idButton : Button = findViewById(R.id.idButton)
        val idField : EditText = findViewById(R.id.idField)
        val activitiesSpinner = findViewById<Spinner>(R.id.labelSpinner)

        //Ask user ID if it does not already exist
        val idFile = getDir("userID", 0)
        if(!File(idFile, "userID.txt").exists()){
            setId(idFile)
        } else {
            val userID = File(getDir("userID", 0), "userID.txt").readText()
            idText.text = "userID is: $userID"
            idButton.visibility = View.GONE
            idField.visibility = View.GONE
        }

        //Change ID button
        changeId.setOnClickListener {
            setId(idFile)
        }

        //Dropdown menu consisting of the activities
        val activities = arrayOf<String>("Recording", "Sitting", "Standing", "Walking", "Running", "Walking stairs")
        if (activitiesSpinner != null){
            val adapter = ArrayAdapter(this,
            android.R.layout.simple_spinner_item, activities)
            activitiesSpinner.adapter = adapter
        }

        //When transmit button is clicked go to the transmit screen
        recordButton.setOnClickListener{
            val intent = Intent(recordButton.context, TransmitActivity::class.java)
            //Put selected activity in the intent
            intent.putExtra("activity", activitiesSpinner.selectedItem.toString())
            recordButton.context.startActivity(intent)
        }
    }

    private fun setId(idFile: File){
        val recordText : TextView = findViewById(R.id.recordText)
        val recordButton : TextView = findViewById(R.id.recordButton)
        val changeId : Button = findViewById(ChangeIdButton)
        val idText : TextView = findViewById(R.id.idText)
        val idButton : Button = findViewById(R.id.idButton)
        val idField : EditText = findViewById(R.id.idField)
        val activitiesSpinner = findViewById<Spinner>(R.id.labelSpinner)

        //Show relevant UI elements
        idButton.visibility = View.VISIBLE
        idField.visibility = View.VISIBLE
        recordText.visibility = View.GONE
        recordButton.visibility = View.GONE
        changeId.visibility = View.GONE
        activitiesSpinner.visibility = View.GONE

        //Change ID when button is clicked
        idButton.setOnClickListener{
            val userID = idField.text.toString()
            File(idFile, "userID.txt").writeText(userID)
            idText.text = "userID is: $userID"
            idButton.visibility = View.GONE
            idField.visibility = View.GONE
            activitiesSpinner.visibility = View.VISIBLE
            recordButton.visibility = View.VISIBLE
            recordText.visibility = View.VISIBLE
            changeId.visibility = View.VISIBLE
            setupPermissions()
        }
    }

    //Setup permission for heartbeat sensor
    private fun setupPermissions() {
        val permission = ContextCompat.checkSelfPermission(this,
            Manifest.permission.BODY_SENSORS)

        if (permission != PackageManager.PERMISSION_GRANTED) {
            makeRequest()
        }
    }

    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<String>, grantResults: IntArray) {
        val textaccel: TextView = findViewById(R.id.recordText)
        when (requestCode) {
            reqcode -> {
                if (grantResults.isEmpty() || grantResults[0] != PackageManager.PERMISSION_GRANTED) {
                    Log.i(ContentValues.TAG, "Permission has been denied by user")
                    textaccel.text = "Pemission denied, please enable senors manually"
                }
            }
        }
    }

    private fun makeRequest() {
        ActivityCompat.requestPermissions(this,
            arrayOf(Manifest.permission.BODY_SENSORS),
            reqcode)
    }
}

