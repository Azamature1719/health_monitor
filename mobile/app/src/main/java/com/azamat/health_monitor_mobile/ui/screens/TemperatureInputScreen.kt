package com.azamat.health_monitor_mobile.ui.screens

import android.util.Log
import androidx.compose.foundation.layout.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.wear.compose.material.*
import java.time.LocalDate
import java.time.format.DateTimeFormatter

@Composable
fun TemperatureInputScreen(
    onSubmit: (Float) -> Unit
) {
    Log.d("TemperatureInputScreen", "TemperatureInputScreen отображён")
    val minInt = 34
    val maxInt = 42
    val minDec = 0
    val maxDec = 9
    val intOptions = (minInt..maxInt).toList()
    val decimalOptions = (minDec..maxDec).toList()

    // Picker states
    val intState = rememberPickerState(
        initialNumberOfOptions = intOptions.size,
        initiallySelectedOption = intOptions.indexOf(36)
    )

    val decimalState = rememberPickerState(
        initialNumberOfOptions = decimalOptions.size,
        initiallySelectedOption = decimalOptions.indexOf(6)
    )

    // Selected values
    var integerPart by remember { mutableStateOf(36) }
    var decimalPart by remember { mutableStateOf(6) }

    // Sync PickerState -> State
    LaunchedEffect(intState.selectedOption) {
        integerPart = intOptions[intState.selectedOption]
    }
    LaunchedEffect(decimalState.selectedOption) {
        decimalPart = decimalOptions[decimalState.selectedOption]
    }

    Scaffold(
        timeText = { TimeText() }
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(vertical = 12.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.SpaceEvenly
        ) {
            // Label
            Text(
                text = "Температура тела",
                fontSize = 16.sp,
                fontWeight = FontWeight.Bold
            )

            // Pickers
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.Center
            ) {
                Picker(
                    state = intState,
                    modifier = Modifier.size(60.dp, 100.dp),
                    contentDescription = "Целая часть температуры",
                    option = { index ->
                        if(integerPart <= 34 || integerPart >= 42){
                            Text(
                                text = "${intOptions[index]}",
                                color = Color.Red,
                                fontSize = 26.sp
                            )
                        }
                        else{
                            Text(
                                text = "${intOptions[index]}",
                                color = Color.White,
                                fontSize = 26.sp
                            )
                        }
                    }
                )

                Text(
                    text = ".", fontSize = 24.sp, color = Color.White,
                    modifier = Modifier.padding(horizontal = 4.dp)
                )

                Picker(
                    state = decimalState,
                    modifier = Modifier.size(60.dp, 100.dp),
                    contentDescription = "Дробная часть температуры",

                    option = { index ->
                        if (integerPart <= 34 || integerPart >= 42) {
                            Text(
                                text = "${decimalOptions[index]}",
                                color = Color.Red,
                                fontSize = 26.sp
                            )
                        } else {
                            Text(
                                text = "${decimalOptions[index]}",
                                color = Color.White,
                                fontSize = 26.sp
                            )
                        }
                    }
                )
            }

            // Submit button
            Button(
                onClick = {
                    val temperature = "$integerPart.$decimalPart".toFloat()
                    onSubmit(temperature)
                },
                modifier = Modifier.size(120.dp, 40.dp)
            ) {
                Text("Отправить")
            }
        }
    }
}
