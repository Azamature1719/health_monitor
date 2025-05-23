/* While this template provides a good starting point for using Wear Compose, you can always
 * take a look at https://github.com/android/wear-os-samples/tree/main/ComposeStarter to find the
 * most up to date changes to the libraries and their usages.
 */

package com.azamat.health_monitor_mobile.ui

import android.os.Bundle
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.core.splashscreen.SplashScreen.Companion.installSplashScreen
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.toLowerCase
import androidx.compose.ui.tooling.preview.Preview
import androidx.wear.compose.material.MaterialTheme
import androidx.wear.compose.material.Text
import androidx.wear.compose.material.TimeText
import androidx.wear.compose.navigation.SwipeDismissableNavHost
import androidx.wear.compose.navigation.composable
import androidx.wear.compose.navigation.rememberSwipeDismissableNavController
import androidx.wear.tooling.preview.devices.WearDevices
import com.azamat.health_monitor_mobile.R
import com.azamat.health_monitor_mobile.ui.screens.OrderScreen
import com.azamat.health_monitor_mobile.ui.screens.TaskListScreen
import com.azamat.health_monitor_mobile.ui.screens.TemperatureInputScreen
import com.azamat.health_monitor_mobile.ui.screens.route.MoodInputRoute
import com.azamat.health_monitor_mobile.ui.screens.route.PressureInputRoute
import com.azamat.health_monitor_mobile.ui.screens.route.TaskDoneRoute
import com.azamat.health_monitor_mobile.ui.screens.route.TaskListRoute
import com.azamat.health_monitor_mobile.ui.screens.route.TemperatureInputRoute
import com.azamat.health_monitor_mobile.ui.theme.Health_monitor_mobileTheme
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        installSplashScreen()

        super.onCreate(savedInstanceState)

        setTheme(android.R.style.Theme_DeviceDefault)

        setContent {
            WearApp()
        }
    }
}

@Composable
fun WearApp() {
    val navController = rememberSwipeDismissableNavController()

    SwipeDismissableNavHost(
        navController = navController,
        startDestination = "tasks"
    ) {

        composable("tasks") {
            TaskListRoute(
                onTaskClick = { task ->
                    navController.navigate("task/${task.id}/${task.type.toString()}")
                }
            )
        }

        composable("task/{id}/temperature") { backStackEntry ->
            val taskId = backStackEntry.arguments?.getString("id")?.toIntOrNull()
            if (taskId != null) {
                Log.d("MainActivity", "Переход на TemperatureInputRoute для taskId=$taskId")
                TemperatureInputRoute(
                    taskId = taskId,
                    onSubmit = {
                        Log.d("MainActivity", "Переход на TaskDoneRoute для taskId=$taskId")
                        navController.navigate("task/$taskId/done")
                    }
                )
            }
        }

        composable("task/{id}/pressure"){ backStackEntry ->
            val taskId = backStackEntry.arguments?.getString("id")?.toIntOrNull()
            if (taskId != null) {
                Log.d("MainActivity", "Переход на PressureInputRoute для taskId=$taskId")
                PressureInputRoute(
                    taskId = taskId,
                    onSubmit = {
                        Log.d("MainActivity", "Переход на TaskDoneRoute для taskId=$taskId")
                        navController.navigate("task/$taskId/done")
                    }
                )
            }
        }

        composable("task/{id}/mood") { backStackEntry ->
            val taskId = backStackEntry.arguments?.getString("id")?.toIntOrNull()
            if (taskId != null) {
                Log.d("MainActivity", "Переход на MoodInputRoute для taskId=$taskId")
                MoodInputRoute(
                    taskId = taskId,
                    onSubmit = {
                        Log.d("MainActivity", "Переход на TaskDoneRoute для taskId=$taskId")
                        navController.navigate("task/$taskId/done")
                    }
                )
            }
        }

        composable("task/{id}/done"){ backStackEntry ->
            val taskId = backStackEntry.arguments?.getString("id")?.toIntOrNull()
            Log.d("MainActivity", "Совершён переход на TaskDone для taskId=$taskId")
            if (taskId != null){
                TaskDoneRoute(
                    taskId = taskId,
                    onSubmit = {
                        Log.d("MainActivity", "Переход на Tasks для taskId=$taskId")
                        navController.navigate("tasks") { popUpTo(navController.graph.startDestinationId) {
                            inclusive = true
                        }
                        }
                    }
                )
            }
        }
    }
}
@Composable
fun Greeting(greetingName: String) {
    Text(
        modifier = Modifier.fillMaxWidth(),
        textAlign = TextAlign.Center,
        color = MaterialTheme.colors.primary,
        text = stringResource(R.string.hello_world, greetingName)
    )
}

@Preview(device = WearDevices.SMALL_ROUND, showSystemUi = true)
@Composable
fun DefaultPreview() {
    WearApp()
}