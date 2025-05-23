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
import com.azamat.health_monitor_mobile.domain.model.MoodChars


@Composable
fun MoodInputScreen(
    onSubmit: (Float) -> Unit
) {
    Log.d("MoodInputScreen", "MoodInputScreen отображён")

    val moodOptions = (MoodChars.MIN_MOOD..MoodChars.MAX_MOOD).toList()

    val moodState = rememberPickerState(
        initialNumberOfOptions = moodOptions.size,
        initiallySelectedOption = moodOptions.indexOf(MoodChars.AVERAGE_MOOD)
    )

    var moodPart by remember { mutableStateOf(MoodChars.AVERAGE_MOOD) }

    LaunchedEffect(moodState.selectedOption) {
        moodPart = moodOptions[moodState.selectedOption]
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
                text = "Уровень\nнастроения",
                textAlign = TextAlign.Center,
                fontSize = 18.sp,
                fontWeight = FontWeight.Bold,

            )

            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.Center,
                modifier = Modifier
                    .padding(vertical = 5.dp)
            ) {
                Picker(
                    state = moodState,
                    modifier = Modifier.size(60.dp, 100.dp),
                    contentDescription = "Уровень настроения",
                    option = { index ->
                        Text(
                            text = "${moodOptions[index]}",
                            color = Color.White,
                            fontSize = 26.sp
                        )
                    }
                )

            }

            Button(
                onClick = {
                    val mood = "$moodPart".toFloat()
                    onSubmit(mood)
                },
                modifier = Modifier.size(120.dp, 40.dp)
            ) {
                Text("Отправить")
            }
        }
    }
}
