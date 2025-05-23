package com.azamat.health_monitor_mobile.ui.screens

import android.util.Log
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.wear.compose.material.Button
import androidx.wear.compose.material.Picker
import androidx.wear.compose.material.Scaffold
import androidx.wear.compose.material.Text
import androidx.wear.compose.material.TimeText
import androidx.wear.compose.material.rememberPickerState
import com.azamat.health_monitor_mobile.domain.model.PressureChars


@Composable
fun PressureInputScreen(
    onSubmit: (Float) -> Unit
) {
    Log.d("PressureInputScreen", "PressureInputScreen отображён")

    val sisOptions = (PressureChars.MIN_SIS .. PressureChars.MAX_SIS).toList()
    val diasOptions = (PressureChars.MIN_DIAS..PressureChars.MAX_DIAS).toList()

    val sisState = rememberPickerState(
        initialNumberOfOptions = sisOptions.size,
        initiallySelectedOption = sisOptions.indexOf(PressureChars.NORMAL_SIS)
    )

    val diasState = rememberPickerState(
        initialNumberOfOptions = diasOptions.size,
        initiallySelectedOption = diasOptions.indexOf(PressureChars.NORMAL_DIAS)
    )

    var sisPart by remember { mutableStateOf(PressureChars.NORMAL_SIS) }
    var diasPart by remember { mutableStateOf(PressureChars.NORMAL_DIAS) }

    LaunchedEffect(sisState.selectedOption) {
        sisPart = sisOptions[sisState.selectedOption]
    }
    LaunchedEffect(diasState.selectedOption) {
        diasPart = diasOptions[diasState.selectedOption]
    }

    Scaffold(
        timeText = { TimeText() }
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(vertical = 20.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.SpaceEvenly
        ) {
            Text(
                text = "Артериальное\nдавление",
                textAlign = TextAlign.Center,
                fontSize = 16.sp,
                fontWeight = FontWeight.Bold,

            )

            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.Center,
                modifier = Modifier
                    .padding(vertical = 5.dp)
            ) {
                Picker(
                    state = sisState,
                    modifier = Modifier.size(60.dp, 100.dp),
                    contentDescription = "Систолическое давление",
                    option = { index ->
                        if(sisPart <= PressureChars.MIN_SIS_CRIT || sisPart >= PressureChars.MAX_SIS_CRIT){
                            Text(
                                text = "${sisOptions[index]}",
                                color = Color.Red,
                                fontSize = 26.sp
                            )
                        }
                        else{
                            Text(
                                text = "${sisOptions[index]}",
                                color = Color.White,
                                fontSize = 26.sp
                            )
                        }
                    }
                )

                Text(
                    text = "/", fontSize = 24.sp, color = Color.White,
                    modifier = Modifier.padding(horizontal = 4.dp)
                )

                Picker(
                    state = diasState,
                    modifier = Modifier.size(60.dp, 100.dp),
                    contentDescription = "Диастолическое давление",

                    option = { index ->
                        if (diasPart <= PressureChars.MIN_DIAS_CRIT || diasPart >= PressureChars.MAX_DIAS_CRIT) {
                            Text(
                                text = "${diasOptions[index]}",
                                color = Color.Red,
                                fontSize = 26.sp
                            )
                        } else {
                            Text(
                                text = "${diasOptions[index]}",
                                color = Color.White,
                                fontSize = 26.sp
                            )
                        }
                    }
                )
            }

            Button(
                onClick = {
                    val pressure = "$sisPart.$diasPart".toFloat()
                    onSubmit(pressure)
                },
                modifier = Modifier.size(120.dp, 40.dp)
            ) {
                Text("Отправить")
            }
        }
    }
}
