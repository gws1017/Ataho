1. 게임의 소개

   제목 : <strong>아타호</strong> 

   <ul>원게임제목 : 환세취호전</ul>
   <ul>"컴파일"에서 만든 게임 , RPG장르</ul>
   <ul>1997년에 출시한 고전 게임이다.</ul>

   ![image](https://github.com/gws1017/2DGP_Term/assets/65538479/458a7e38-401a-4abe-8028-fcc7e15d7435)

   ![image](https://github.com/gws1017/2DGP_Term/assets/65538479/8f14e754-9dc7-417b-ae5a-6d92a58092ab)

   ![image](https://github.com/gws1017/2DGP_Term/assets/65538479/a29cfe57-6dfa-4260-a3f2-88726412fcb7)

   

   ---

2. GameState (Scene)

   - 로고 스테이트

   - 타이틀 스테이트
   - 마을, 필드1, 필드2 스테이트 (맵)
   - ~~스테이터스 / 설정 스테이트~~
   - 전투 스테이트
   - 엔딩

   ---

3. GameState 설명

   <img src="https://user-images.githubusercontent.com/65538479/94275454-f08f2b00-ff81-11ea-8608-0124b998dc21.JPG" alt="설명"  />

   - 타이틀에서 스페이스를 입력하면 새로시작 하거나 저장된 지점부터 이어서 할 수 있다.

     게임을 시작하면  마을에서 시작한다. 마을에는 저장을 위한 **세이브 오브젝트**, ~~**NPC (상인)**~~이 표시된다.

     항상 화면 아래쪽은 **캐릭터이름 HP MP EXP 장소**이 표시된다.

     **필드1** 에는 아무것도 없으나 계속 돌아다니면 전투에 돌입한다. (포켓몬스터 형식), ~~**아이템**이 간혹 떨어져있기도함~~

     **필드2** 에도  필드1과 비슷하나 가운데에 **보스NPC**가 서있고 상호작용 시 언제든지 도전이 가능하다

     보스를 클리어하면 엔딩 스테이트로 변경

     전투 스테이트 에서는 왼쪽에 **주인공 객체** 오른쪽에 **몬스터(1~3마리)객체**들이 존재합니다.

     턴 형식으로 공격되는데 기술/아이템사용 중 하나를 선택해 정합니다.

     키는 전부 "<strong>방향키</strong>", "**SPACE**" 로 조작합니다.

   ---

4. 필요한 기술

   - 다른 과목에서 배운 기술 

     윈도우 프로그래밍 - **카메라 이동**

   - 이 과목에서 배울 것으로 기대되는 기술

     **사운드** 출력 및 처리

   - 다루지 않는 것 같아서 수업에 다루어 달라고 요청할 기술

     BMP 리소스를 사용할경우 배경색이 존재하는데 해당색을 투명처리후 드로우 하는 법 (윈도우 프로그래밍의 **TransparentBIT** 함수와 같은 기능)

     몬스터의 전투 **AI** (간단히) ex) 일반적인 경우에는 공격을 하지만, HP가 빈사상태라면 방어를 한다.(2회 이하)

     게임데이터를 dat 파일로 저장해 **세이브 파일**을 만들어서 언제든지 이어서 할 있는 기능
   
   ------
   
5. 게임 컨셉

   + 고전 게임 "환세취호전"의 모작

   + 턴제 RPG게임

   + 반복적인 전투로 스펙을 쌓아서 최종보스를 무찌르는 게임

     

6. 개발 범위

   |   내용   |                           최소범위                           |         추가범위          |
   | :------: | :----------------------------------------------------------: | :-----------------------: |
   |  캐릭터  |             이동, 오브젝트 상호작용, 스테이터스              |             X             |
   |   기술   | 개인공격기(단일공격) <span style="color:red">~~3개~~이상 → **2개**</span>, 기술 등급에따라 이펙트, 데미지 차이 | 상태이상, 전체공격기 추가 |
   |    맵    |    마을, 필드2가지, 엔딩화면, 전투화면, 시작화면,설정화면    |             X             |
   |  몬스터  |            일반몬스터 2가지이상, 보스몬스터 1가지            |    보스몬스터 2페이즈     |
   | 오브젝트 |              석상(세이브 포인트), ~~상점 NPC~~               |  숨겨진 오브젝트(아이템)  |
   |  아이템  |                       ~~회복 아이템~~                        |             X             |
   |   전투   |                     적 공격 , 전투 진행                      |    적 공격 로직 다양화    |

7. 게임 실행 흐름

   ###### 1. 마을

   ![image](https://github.com/gws1017/2DGP_Term/assets/65538479/171931d5-da78-4dc4-8b89-69ae5160e41d)!![image](https://github.com/gws1017/2DGP_Term/assets/65538479/ac1c1421-6d0f-45bc-9416-792f7e54df82)

   게임은 마을에서 시작합니다. 

   마을에서만 게임을 저장할 수 있고, 석상과는 상호작용 시 체력이 회복됩니다.

   

   ######  2.전투

   ![image](https://github.com/gws1017/2DGP_Term/assets/65538479/2f8296c4-e3f1-4f67-96e9-34b5a1c34375)

   왼쪽이 **필드**가 되고 오른쪽이 **전투 화면**입니다.

   필드에서 계속 돌아다니면 전투에 돌입하게되고 오른쪽화면으로 바뀌게됩니다.

   전투는 턴제로 자신이 어떤행동을 할지 정한 후 적과 자신의 캐릭터가 한번씩 행동을하고 다시 행동을 선택하는 방식입니다.

   전투에서 승리하면 경험치와 소량의 돈을 획득합니다.

   

   ###### 	3.보스

   ![image](https://github.com/gws1017/2DGP_Term/assets/65538479/b14d416f-4dba-47fe-a6bd-0ee49166e701)

   **보스**는 마지막필드에 위치해있으며 언제든지 도전이 가능하고 상호작용 시 전투 화면으로 넘어가게됩니다.

   보스를 잡으면 게임이 끝나 엔딩화면이 나오게 됩니다.

   

8. **개발 일정**

   | 주차  | 구현 항목                                              | 세부 내용                                                    |
   | ----- | ------------------------------------------------------ | ------------------------------------------------------------ |
   | 1주차 | <span style="color:red">(100%)</span>리소스            | 리소스 배경색 투명으로 바꾸기, 맵그리기(마을,필드)           |
   | 2주차 | <span style="color:red">(90%)</span>오브젝트           | 캐릭터 이동 ,스텟(HP,MP,EXP,공격력,레벨 등), ~~아이템~~      |
   | 3주차 | <span style="color:red">(100%)</span>점검 및 기본 토대 | 게임 프레임워크 마련,  부족한점 보완                         |
   | 4주차 | <span style="color:red">(100%)</span>전투              | 전투 체계 수립(전투 시작 조건, 턴 돌아가는 방식,몬스터 공격) |
   | 5주차 | <span style="color:red">(100%)</span>애니메이션        | 기술 애니메이션 구현 , 일반 몬스터 애니메이션 구현           |
   | 6주차 | <span style="color:red">(100%)</span>보스              | 보스 애니메이션, 상호작용, 보스 공격                         |
   | 7주차 | <span style="color:red">(80%)</span>기타기능           | ~~상점~~, 저장, ~~설정화면~~, 사운드 구현, 엔딩 화면         |
   | 8주차 | 마무리                                                 | 최종 점검 및 추가 구현                                       |

   
   
9. **주차별 커밋 통계**

   ![image](https://user-images.githubusercontent.com/65538479/101104118-c2773880-360d-11eb-897c-09e1903fecf1.png)

   | 주차  | 횟수 |
   | :---: | :--: |
   | 1주차 | 3회  |
   | 2주차 | 0회  |
   | 3주차 | 3회  |
   | 4주차 | 7회  |
   | 5주차 | 5회  |
   | 6주차 | 2회  |
   | 7주차 | 12회 |
   | 8주차 | 4회  |
   | 총계  | 36회 |

   

