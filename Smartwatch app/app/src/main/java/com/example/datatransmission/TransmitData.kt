package com.example.datatransmission

import android.util.Log
import com.squareup.moshi.Json
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.converter.moshi.MoshiConverterFactory
import java.util.concurrent.TimeUnit


class TransmissionService{
    private val interceptor = HttpLoggingInterceptor().setLevel(HttpLoggingInterceptor.Level.NONE)

    private val okHttpClient = OkHttpClient.Builder()
        .addInterceptor(interceptor)
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .build()

    private val retrofit = Retrofit.Builder()
        .client(okHttpClient)
//        .baseUrl("http://shijie.pythonanywhere.com/")
        .baseUrl("http://marijn.ddns.net/")
        .addConverterFactory(MoshiConverterFactory.create())
        .build()


    //create Service
    private val service = retrofit.create(APIService::class.java)

    fun transmitData(Data: Data) {

        CoroutineScope(Dispatchers.IO).launch {

//            val time = Data.last().timestamp.toString()
//            Log.d("Time:", time)

            //Do the POST request and get response
            val response = service.sendData(Data)

//            Log.d("request", "${interceptor.toString()}")

            if (response.isSuccessful) {
                Log.d("Response :", "${response.message()}, Time: ${Data.timestamp}")
            } else {
                Log.e("RETROFIT_ERROR", response.code().toString())
            }
        }
    }
}