import 'package:flutter/material.dart';

class CreedScreen extends StatefulWidget {
  const CreedScreen({super.key});

  @override
  State<CreedScreen> createState() => _CreedScreenState();
}

class _CreedScreenState extends State<CreedScreen> {
  int _version = 0; // 0: 개역개정, 1: 개역한글

  final Map<int, String> _versions = {
    0: '''나는 전능하신 아버지 하나님, 천지의 창조주를 믿습니다.
나는 그의 유일하신 아들, 우리 주 예수 그리스도를 믿습니다.
그는 성령으로 잉태되어 동정녀 마리아에게서 나시고
본디오 빌라도에게 고난을 받아 십자가에 못 박혀 죽으시고
장사된 지 사흘 만에 죽은 자 가운데서 다시 살아나셨으며
하늘에 오르시어 전능하신 아버지 하나님 우편에 앉아 계시다가
거기로부터 살아 있는 자와 죽은 자를 심판하러 오십니다.
나는 성령을 믿으며 거룩한 공교회와 성도의 교제와
죄를 용서받는 것과 몸의 부활과 영생을 믿습니다. 아멘.''',
    1: '''전능하사 천지를 만드신 하나님 아버지를 내가 믿사오며,
그 외아들 우리 주 예수 그리스도를 믿사오니,
이는 성령으로 잉태하사 동정녀 마리아에게 나시고,
본디오 빌라도에게 고난을 받으사 십자가에 못 박혀 죽으시고,
장사한 지 사흘 만에 죽은 자 가운데서 다시 살아나시며,
하늘에 오르사 전능하신 하나님 우편에 앉아 계시다가,
저리로서 산 자와 죽은 자를 심판하러 오시리라.
성령을 믿사오며, 거룩한 공회와 성도가 서로 교통하는 것과,
죄를 사하여 주시는 것과, 몸이 다시 사는 것과,
영원히 사는 것을 믿사옵나이다. 아멘.''',
  };

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('사도신경'),
        bottom: PreferredSize(
          preferredSize: const Size.fromHeight(40),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              ChoiceChip(
                label: const Text('개역개정'),
                selected: _version == 0,
                onSelected: (_) => setState(() => _version = 0),
              ),
              const SizedBox(width: 8),
              ChoiceChip(
                label: const Text('개역한글'),
                selected: _version == 1,
                onSelected: (_) => setState(() => _version = 1),
              ),
            ],
          ),
        ),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: SingleChildScrollView(
          child: SelectableText(
            _versions[_version]!.trim(),
            style: const TextStyle(fontSize: 18, height: 1.8),
          ),
        ),
      ),
    );
  }
}
